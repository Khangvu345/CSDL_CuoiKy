import pymysql
from contextlib import contextmanager

def get_db():
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="HocSQL@155@",
        database="testCSDL",
        cursorclass=pymysql.cursors.DictCursor,
        charset="utf8mb4",
        autocommit=True,
    )
    try:
        yield connection
    finally:
        connection.close()