import sqlite3
import os


class SqliteDb:
    """

    """
    def __init__(self, db_name="2gis.db"):
        self.db_name = db_name
        self.dir_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.db_name)

    def create_db(self):
        """

        :return:
        """
        with open(self.dir_data, "w+") as db:
            db.close()

    def connect_sqlite(self):
        """

        :return:
        """
        return sqlite3.connect(self.dir_data)

    def cursor_db(self):
        """

        :return:
        """
        return self.connect_sqlite().cursor()

    def execute_db(self, sql, params=(), commit_db=False):
        """

        :param sql:
        :param params:
        :param commit_db:
        :return:
        """
        con = self.connect_sqlite()

        if commit_db:
            con.execute(sql, params)
            con.commit()
        else:
            return con.execute(sql, params)

    def create_data_urls(self, data, config_table_urls):
        """

        :param data:
        :param config_table_urls:
        :return:
        """
        table, column = config_table_urls
        check_table = f"""select * from {table}"""
        create_table = f"""
            CREATE TABLE {table} (
            PK INTEGER NOT NULL, 
            URL TEXT, 
            {column[0].upper()} TEXT, 
            {column[1].upper()} TEXT, 
            {column[2].upper()} TEXT, 
            DATE_ADD TEXT,
            DATE_UPDATE TEXT,
            PRIMARY KEY (PK))
         """

        try:
            self.execute_db(check_table)
        except Exception as e:
            if "no such table" in e.args[0]:
                self.execute_db(create_table.format(table=table, *column), commit_db=True)

        data_urls = (i for i in list(data))

        for url in data_urls:
            write_data = f"""insert into {table} (url, date_add) values (?, datetime('now','localtime'))"""
            self.execute_db(write_data, (url,), commit_db=True)
