import sqlite3
import os


class SqliteDb:
    def __init__(self, db_name="2gis.db"):
        self.db_name = db_name
        self.dir_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.db_name)

    def create_db(self):
        with open(self.dir_data, "w+") as db:
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

    def create_data_urls(self, data, config_table_urls):
        table, column = config_table_urls
        con = self.connect_sqlite()
        check_table = f"""select * from {table}"""
        create_table = f"""CREATE TABLE {table} (PK INTEGER NOT NULL, url TEXT, {column[0]} TEXT, {column[1]} TEXT, {column[2]} TEXT, PRIMARY KEY (PK))"""

        try:
            self.execute_db(check_table)
        except Exception as e:
            if "no such table" in e.args[0]:
                self.execute_db(create_table.format(table=table, *column), commit_db=True)

        data_urls = (i for i in list(data))

        for url in data_urls:
            write_data = f"""insert into {table} (url) values (?)"""
            self.execute_db(write_data, (url,), commit_db=True)

