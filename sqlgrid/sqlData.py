import sqlalchemy
from sqlalchemy.sql import text
import pandas as pd

class sqlData():
    """
    sqlData class is the adapter between sqlgridWidget and an SQL DataSource
    New type accepted by the show_grid function which creates a Grid Widget

    Parameters
    ----------
        path: string
            SQLAlchemy connection string to access the database
        table: string
            which table of the database is targeted
        page: integer
            should be the same value as PAGE_SIZE in grid.py
        out: ipywidget.output
            if one wants to output some information (it's for debug)
        filter: list
            list of columns to filter from the table

    See Also
    --------
        sqlgrid.show_grid: 
             open an sqlgrid in jupyter Lab notebook
    
    Notes
    -----
    How to set breakpoints in this code (usable in Jupyter Notebooks)::
 
        import ipdb; ipdb.set_trace()
        # don't always works however

    """
    def __init__(self, path=None, table=None, page=100, out=None, filter=None):
        self.path = path
        self.page = page
        self.engine = None
        self.position = 0
        self.table = table
        if path is not None:
            self.engine = sqlalchemy.create_engine(path)
            with self.engine.connect() as conn:
                statement = text(f"SELECT count(*) FROM `{self.table}`")
                self.tablesize = conn.execute(statement).fetchone()[0]
                statement = text(f"SELECT * FROM `{self.table}` LIMIT 1")
                self.columnNames = conn.execute(statement).fetchone().keys()
        self._widget = None
        self.out = out
        self.filter = filter

    def set_filter(self, filter):
        self.position = 0
        self.filter = filter

    def getColumns(self):
        """
        Using the self.filter list, returns an SQL compliant column list
        Adds the index clolumn if existing in the database table

        Parameters
        ----------
            self.filter: list
                The list of column to filter the database table

        Returns
        -------
            string
                An SQL compliant, comma separated and backtick quoted, list of columns
        """
        _filter = ""
        if self.filter is None or len(self.filter) == 0:
            _filter = "*"
            return _filter

        if 'index' in self.columnNames:
            _filter = "`index`"

        for col in self.filter:
            if _filter == "":
                _filter = f"`{col}`"
            else:
                _filter = _filter + f", `{col}`"

        return _filter

    def _update_df(self, _index_col_name, overlap=0):
        """
        Returns the database table slice, as a DataFrame, according to the underlying grid state
        * save the _index_column_name as an instance variable
        * add a column named '_index_column_name' to the result DataFrame

        Parameters
        ----------
            _index_col_name: string
               name of the column which will be added to the resulting DataFrame and needed by the grid
            overlap: integer
               number of overlaping rows
            self.table: 
               the name of the table to work with
            self.page: 
               the page size to crop when reading the database table
            self.position: 
               where is the table cursor located
            self.engine: 
               the database SQLAlchemy engine connection

        Returns
        -------
            DataFrame
               the table slice as a pandas DataFrame
        
        See Also
        --------
            sqlData.getColumns: to get the list of column to return
            sqlData.where: to get the WHERE sub-statement to filter the resulting rows
            sqlData.order_by: to get the Order By sub-statement
        """
        self._index_col_name = _index_col_name
        _df = pd.read_sql(f"SELECT {self.getColumns()} FROM `{self.table}` {self.where()} {self.order_by()} LIMIT {self.page+abs(overlap)} OFFSET {self.position+overlap}",
                          self.engine
                         )
        # insert a column which we'll use later to map edits from
        # a filtered version of this df back to the unfiltered version
        _df.insert(0, _index_col_name, range(self.position, self.position+len(_df)))
        return _df
     
    def order_by(self):
        """
        Using bound grid state, returns the SQL "ORDER BY" sub-statement

        Parameters
        ----------
            self._widget._sort_field: string
                which column to sort with
            self._widget._sort_ascending: boolean
                if True, set 'ASC' if False, set 'DESC'

        Returns
        -------
            string
                the sql "ORDER BY" sub-statement or "" if no order directive set
        """
        _order_by = ""
        if self._widget is not None:
            if self._widget._sort_field is not None and len(self._widget._sort_field) != 0:
                _order_by = f"ORDER BY `{self._widget._sort_field}`"
                if self._widget._sort_ascending:
                    _order_by = _order_by + " ASC"
                else:
                     _order_by = _order_by + " DESC"
        if len(_order_by) != 0:
            pass
            #with self.out:
                #print(f"order_by = {_order_by}")

        return _order_by

    def where(self, exclude=[]):
        """
        Using bound grid state, returns the SQL "WHERE" sub-statement or "" if no filtering set

        Parameters
        ----------
            exclude: list,(default=[])
                    list of columns to exclude when calculating where
            self._widget._columns: list
                    list of grid's columns
            self._widget_filter_tables: list
                    filters set via the grid gui (can exist or not for a given column)
            self._widget._columns[col]['filter_info']: dict
                    holds the filter type and other descriptors depending upon type

        Returns
        -------
            string
                  the sql "WHERE" sub-statement or "" if no filtering conditions are set
        """
        _where = ""
        if self._widget is None:
            return _where
        columns = self._widget._columns
        _filter_tables = self._widget._filter_tables
        for col in list(columns.keys()):
            if col in _filter_tables and col not in exclude and 'filter_info' in columns[col]:
                if columns[col]['filter_info']['type'] == 'text' \
                        and 'selected' in columns[col]['filter_info'] \
                        and columns[col]['filter_info']['selected'] is not None \
                        and columns[col]['filter_info']['selected'] != 'all':
                    incol = [f"'{_filter_tables[col][i]}'" for i in columns[col]['filter_info']['selected']]
                    if len(incol) != 0:
                        addNone = False
                        if "'None'" in incol:
                            incol.remove("'None'")
                            addNone = True
                        if len(_where) > 0:
                            _where = _where + " AND "
                        if addNone:
                            if len(incol) != 0:
                                _where = _where + f"( `{col}` IN (" + ",".join(incol) + f") OR `{col}` IS NULL )"
                            else:
                                _where = _where + f"`{col}` IS NULL"
                        else:
                            _where = _where + f"`{col}` IN (" + ",".join(incol) + ")"
            if 'filter_info' in columns[col] and (columns[col]['filter_info']['type'] == 'date' or columns[col]['filter_info']['type'] == 'slider'):
                if columns[col]['filter_info']['min'] is not None \
                    and columns[col]['filter_info']['max'] is not None:
                    if len(_where) > 0:
                            _where = _where + " AND "
                    _where = _where + f"( `{col}` BETWEEN {columns[col]['filter_info']['min']} AND {columns[col]['filter_info']['max']})"
                if columns[col]['filter_info']['min'] is None \
                    and columns[col]['filter_info']['max'] is not None:
                    if len(_where) > 0:
                            _where = _where + " AND "
                    _where = _where + f"( `{col}` <= {columns[col]['filter_info']['max']})"
                if columns[col]['filter_info']['min'] is not None \
                    and columns[col]['filter_info']['max'] is None:
                    if len(_where) > 0:
                            _where = _where + " AND "
                    _where = _where + f"( `{col}` >= {columns[col]['filter_info']['min']})"
                        

        if len(_where) != 0:
            _where = " WHERE " + _where
            with self.out:
                #print(f"where = {_where}")
                pass
        return _where

    def _update_table(self, _viewport_range, _df, widget):
        """
        Recalculate which database table slice should be provided as the grid's DataFrame

        Parameters
        ----------
            _viewport_range: tuple
                * [0] index low range => if 0 user is moving backward
                * [1] index high range => if > self.page user is moving forward
            _df: DataFrame
                current value of the grid DataFrame (actually not currently used)
            widget: sqlgridWidget
                reference of the underlying grid

        Returns
        -------
            tuple
                (True if moving forward or False if backward, the table slice as a DataFrame)
        """
        self._widget = widget
        if _viewport_range[1] > self.page:
            # load forward
            if self.position + self.page < self.tablesize:
                self.position += self.page
                return (True, self._update_df(self._index_col_name, overlap=-5))
        if _viewport_range[0] == 0:
            # load backward
            if self.position > 0:
                self.position -= self.page
                overlap = 5 if self.position !=0 else 0
                return (False, self._update_df(self._index_col_name, overlap=overlap))
            if self.position == 0:
                return (True, self._update_df(self._index_col_name))
        return (None,None)

    def minmax(self, column):
        """
        Find the minimun and the maximum of an interger or float column

        Parameters
        ----------
            column: string
                which column to calculate (min,max)

        Returns
        -------
            tuple
                (min,max) of a given column
        """
        minmax = (0,0)
        with self.engine.connect() as conn:
            statement = text(f"SELECT min(`{column}`) AS `min`, max(`{column}`) AS `max` FROM `{self.table}`")
            minmax = conn.execute(statement).fetchone()
        return minmax
    
    def distinctValuesOrdered(self, column, otype):
        """
        Get the distinct values of a given column sorted in ascending order

        Parameters
        ----------
            column: string
                Which column to look distinct values for
            otype: string
                column type ('text',...)

        Returns
        -------
            list:
                a list [] of sorted distinct values for the given column, null values are replaced by 'None' for a text column
        """
        values = []
        with self.engine.connect() as conn:
            statement = text(f"SELECT DISTINCT `{column}` FROM `{self.table}` {self.where(exclude=[column])} ORDER BY `{column}`")
            result = conn.execute(statement).fetchall()
            if otype == 'text':
                values = [str(r[0]) for r in result]
        return values
       
        



