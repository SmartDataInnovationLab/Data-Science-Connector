import queue
import sqlite3
import aiosql
import os
from sqlite3 import Error

from app.constants import DB_FILE_PATH

SQL_DIR = os.path.join(os.path.dirname(__file__), 'sql')
queries = aiosql.from_path(SQL_DIR, 'sqlite3')

used_db_file = None


def get_db():
    conn = sqlite3.connect(used_db_file, isolation_level=None)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_file=DB_FILE_PATH):
    global used_db_file
    used_db_file = db_file
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        queries.users.create_schema(conn)
        queries.instances.create_schema(conn)
    # except Error as e:
    #     print(e)
    finally:
        if conn:
            conn.close()