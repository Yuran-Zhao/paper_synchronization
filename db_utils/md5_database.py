import os
import sqlite3
from .base_database import baseDataBase


class MD5DB(baseDataBase):
    def __init__(self, root_dir, db_name='md5'):
        super(MD5DB, self).__init__(root_dir, db_name)
        if not os.path.exists(self.db_path):
            self.init_db()

    def connect_db(self):
        conn = sqlite3.connect(self.db_path)
        return conn, conn.cursor()

    def close_db(self, conn, cursor):
        cursor.close()
        conn.close()

    def init_db(self):
        conn, cursor = self.connect_db()
        cursor.execute('''CREATE TABLE HASH
        (FILENAME TEXT PRIMARY KEY NOT NULL,
        MD5 TEXT NOT NULL);''')
        conn.commit()
        self.close_db(conn, cursor)

    def query(self, filename):
        conn, cursor = self.connect_db()
        cursor.execute("SELECT MD5 FROM HASH WHERE FILENAME=?", (filename, ))
        result = cursor.fetchall()
        assert len(result) < 2
        self.close_db(conn, cursor)
        return result[-1] if len(result) == 1 else None

    def update(self, filename, md5, check_exist=False):
        if (not check_exist) and self.query(filename) is None:
            self.insert(filename, md5)
            return
        conn, cursor = self.connect_db()
        cursor.execute("UPDATE HASH SET MD5=? WHERE FILENAME=?",
                       (md5, filename))
        conn.commit()
        self.close_db(conn, cursor)

    def insert(self, filename, md5):
        if self.query(filename) is not None:
            self.update(filename, md5, check_exist=True)
        else:
            conn, cursor = self.connect_db()
            cursor.execute("INSERT INTO HASH (FILENAME, MD5) VALUES (?, ?)",
                           (filename, md5))
            conn.commit()
            self.close_db(conn, cursor)
            return

    def check_modification(self, filename, cur_md5):
        prev_md5 = self.query(filename)
        return prev_md5 != cur_md5