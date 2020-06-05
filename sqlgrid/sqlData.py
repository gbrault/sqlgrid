import sqlalchemy
from sqlalchemy.sql import text
import pandas as pd

class sqlData():
    """
    sqlgrid class is the adapter between sqlgridWidget and an SQL DataSource
    New type accepted by the show_grid function which creates a Grid Widget
    import ipdb; ipdb.set_trace() (breakpoint!)
    """
    def __init__(self, path=None, table=None, page=100, out=None):
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
        self._widget = None
        self.out = out

    def _update_df(self, _index_col_name, overlap=0):
        self._index_col_name = _index_col_name
        _df = pd.read_sql(f"SELECT * FROM `{self.table}` {self.where()} {self.order_by()} LIMIT {self.page+abs(overlap)} OFFSET {self.position+overlap}",
                          self.engine
                         )
        # insert a column which we'll use later to map edits from
        # a filtered version of this df back to the unfiltered version
        _df.insert(0, _index_col_name, range(self.position, self.position+len(_df)))
        return _df
     
    def order_by(self):
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
                        if len(_where):
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
                    _where = _where + f"( `{col}` BETWEEN {columns[col]['filter_info']['min']} AND {columns[col]['filter_info']['max']})"
                if columns[col]['filter_info']['min'] is None \
                    and columns[col]['filter_info']['max'] is not None:
                    _where = _where + f"( `{col}` <= {columns[col]['filter_info']['max']})"
                if columns[col]['filter_info']['min'] is not None \
                    and columns[col]['filter_info']['max'] is None:
                    _where = _where + f"( `{col}` >= {columns[col]['filter_info']['min']})"
                        

        if len(_where) != 0:
            _where = " WHERE " + _where
            with self.out:
                #print(f"where = {_where}")
                pass
        return _where

    def _update_table(self, _viewport_range, _df, widget):
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
        minmax = (0,0)
        with self.engine.connect() as conn:
            statement = text(f"SELECT min(`{column}`) AS `min`, max(`{column}`) AS `max` FROM `{self.table}`")
            minmax = conn.execute(statement).fetchone()
        return minmax
    
    def distinctValuesOrdered(self, column, otype):
        values = []
        with self.engine.connect() as conn:
            statement = text(f"SELECT DISTINCT `{column}` FROM `{self.table}` {self.where(exclude=[column])} ORDER BY `{column}`")
            result = conn.execute(statement).fetchall()
            if otype == 'text':
                values = [str(r[0]) for r in result]
        return values
       
        



