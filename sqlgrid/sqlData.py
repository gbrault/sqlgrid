import sqlalchemy
from sqlalchemy.sql import text
import pandas as pd

class sqlData():
    """
    sqlgrid class is the adapter between sqlgridWidget and an SQL DataSource
    New type accepted by the show_grid function which creates a Grid Widget
    """
    def __init__(self, path=None, table=None, page=100):
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

    def _update_df(self, _index_col_name):
        self._index_col_name = _index_col_name
        _df = pd.read_sql(f"SELECT * FROM `{self.table}` LIMIT {self.page} OFFSET {self.position}",
                          self.engine
                         )
        # insert a column which we'll use later to map edits from
        # a filtered version of this df back to the unfiltered version
        _df.insert(0, _index_col_name, range(self.position, self.position+len(_df)))
        return _df

    def _update_table(self, _viewport_range, _df):
        if _viewport_range[1] > self.page:
            # load forward
            if self.position + self.page < self.tablesize:
                self.position += self.page
                return self._update_df(self._index_col_name)
        if _viewport_range[0] == 0:
            # load backward
            if self.position > 0:
                self.position -= self.page
                return self._update_df(self._index_col_name)
        return None



