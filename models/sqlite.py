import sqlite3
import os


class SqliteDb:
    def __init__(self, db_name="2gis.db"):
        self.db_name = db_name
        self.dir_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.db_name)

    def create_db(self):
        with open(self.dir_data, "w+") as db:
            print(self.dir_data)
            print("db создана")
            db.close()

    def connect_sqlite(self):
        return sqlite3.connect(self.dir_data)

    def cursor_db(self):
        return self.connect_sqlite().cursor()

    def execute_db(self, sql, params=(), commit_db=False):
        con = self.connect_sqlite()
        con.execute(sql, params)
        if commit_db:
            con.commit()