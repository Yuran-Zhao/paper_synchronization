import sqlite3
import os


class baseDataBase(object):
    def __init__(self, root_dir, db_name):
        self.table_name = db_name.upper()
        self.db_path = os.path.join(root_dir, db_name + '.db')

    def connect_db(self):
        conn = sqlite3.connect(self.db_path)
        return conn, conn.cursor()

    def close_db(self, conn, cursor):
        cursor.close()
        conn.close()

    def init_db(self):
        raise NotImplementedError

    def query(self, q):
        raise NotImplementedError

    def update(self, key, value):
        raise NotImplementedError

    def insert(self, key, value):
        raise NotImplementedError
