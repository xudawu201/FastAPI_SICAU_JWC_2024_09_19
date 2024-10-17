'''
Author: xudawu
Date: 2024-10-17 14:18:25
LastEditors: xudawu
LastEditTime: 2024-10-17 15:34:20
'''
from app.database import database_connection
import pyodbc

# 查表
def select_table(select_sql_str):
    # 获得数据库连接和游标
    DatabaseConnection, DatabaseCursor = database_connection.get_database_connection_cursor()
    if DatabaseConnection and DatabaseCursor:
        try:
            # 执行SQL语句
            DatabaseCursor.execute(select_sql_str)
            # 获取所有行
            rows = DatabaseCursor.fetchall()
            # 返回所有行
            return rows
        except pyodbc.Error as e:
            print(f"SQL Error: {e}")
        finally:
            # 确保关闭游标和连接,先关闭游标再关闭连接
            DatabaseCursor.close()
            DatabaseConnection.close()

# 插入表
def insert_table(insert_sql_str):
    # 获得数据库连接和游标
    DatabaseConnection, DatabaseCursor = database_connection.get_database_connection_cursor()
    if DatabaseConnection and DatabaseCursor:
        try:
            # 执行SQL语句
            DatabaseCursor.execute(insert_sql_str)
            # 提交事务
            DatabaseConnection.commit()
        except pyodbc.Error as e:
            print(f"SQL Error: {e}")
            # 发生错误时回滚事务
            DatabaseConnection.rollback()
        finally:
            # 确保关闭游标和连接,先关闭游标再关闭连接
            DatabaseCursor.close()
            DatabaseConnection.close()