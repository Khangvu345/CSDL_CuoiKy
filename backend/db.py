import pymysql
from contextlib import contextmanager

def get_db():
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="HocSQL@155@",
        database="csdl",
        cursorclass=pymysql.cursors.DictCursor,
        charset="utf8mb4",
        autocommit=True,
        connect_timeout=5
    )
    try:
        yield connection
    finally:
        connection.close()