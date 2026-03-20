# migrate_db.py
import sqlite3
import pandas as pd
import pymysql
import os

#    'NAME': 'dialect_search',
# #         'USER': 'dialect_user',
# #         'PASSWORD': 'mycmyc',
# #         'HOST': 'localhost',
# #         'PORT': '3306',
def migrate_from_mysql_to_sqlite():
    # 连接MySQL
    mysql_conn = pymysql.connect(
        host='localhost',
        user='dialect_user',
        password='mycmyc',
        database='dialect_search'
    )

    # 创建SQLite数据库
    sqlite_conn = sqlite3.connect('db.sqlite3')

    # 获取MySQL表结构
    mysql_cursor = mysql_conn.cursor()
    mysql_cursor.execute("SHOW TABLES")
    tables = mysql_cursor.fetchall()

    # 迁移每个表
    for table in tables:
        table_name = table[0]
        print(f"迁移表: {table_name}")

        # 读取MySQL表数据
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, mysql_conn)

        # 写入SQLite
        df.to_sql(table_name, sqlite_conn, if_exists='replace', index=False)

    mysql_conn.close()
    sqlite_conn.close()

    print("数据迁移完成")


if __name__ == "__main__":
    migrate_from_mysql_to_sqlite()