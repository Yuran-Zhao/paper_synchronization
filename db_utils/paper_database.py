import os
import sqlite3
from .base_database import baseDataBase
from search import search_paper


class paperDB(baseDataBase):
    def __init__(self, root_dir, db_name='paper'):
        super(paperDB, self).__init__(root_dir, db_name)
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
        cursor.execute('''CREATE TABLE PAPER
        (NAME TEXT PRIMARY KEY NOT NULL,
        AUTHOR TEXT ,
        YEAR INT ,
        CITATION INT ,
        );''')
        conn.commit()
        self.close_db(conn, cursor)

    def query(self, papername):
        conn, cursor = self.connect_db()
        cursor.execute("SELECT NAME FROM PAPER WHERE NAME=?", (papername, ))
        result = cursor.fetchall()
        assert len(result) < 2
        self.close_db(conn, cursor)
        return result[-1] if len(result) == 1 else None

    def update(self, papername, author, year, citation):
        conn, cursor = self.connect_db()
        cursor.execute(
            "UPDATE PAPER SET AUTHOR=?, YEAR=?, CITATION=? WHERE NAME=?",
            (author, year, citation, papername))
        conn.commit()
        self.close_db(conn, cursor)

    def insert(self, papername):
        if self.query(papername) is not None:
            return
        conn, cursor = self.connect_db()
        try:
            author, year, citation = search_paper(papername)
        except:
            author, year, citation = None, None, None
        cursor.execute(
            "INSERT INTO PAPER (NAME, AUTHOR, YEAR, CITATION) VALUES (?, ?, ?, ?)",
            (papername, author, year, citation))
        self.close_db(conn, cursor)
        return

    def get_all_saved_papers(self):
        conn, cursor = self.connect_db()
        cursor.execute("SELECT NAME FROM PAPER")
        result = cursor.fetchall()
        self.close_db(conn, cursor)
        return result