import sqlite3


class Models:
    def __init__(self, db_name="2gis.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)

    def create_db(self):
        with open(self.db_name, "w+") as db:
            db.close()
            print("db создана")

    def cursor_db(self):
        return self.conn.cursor()

    def execute_db(self, sql, params=(), commit_db=False):
        cur = self.conn
        cur.execute(sql, params)
        if commit_db:
            self.conn.commit()