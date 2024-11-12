'''
Author: xudawu
Date: 2024-10-17 14:18:25
LastEditors: xudawu
LastEditTime: 2024-11-12 09:04:18
'''
from database import database_connection
import pyodbc

# 查表
def select_table(select_sql_str):
    # 获得数据库连接和游标
    DatabaseConnection, DatabaseCursor = database_connection.get_database_connection_cursor()
    # sql语句执行标志
    excute_sql_flag_str = 'sql执行失败'
    if DatabaseConnection and DatabaseCursor:
        try:
            # 执行SQL语句
            DatabaseCursor.execute(select_sql_str)
            # 获取所有行
            rows = DatabaseCursor.fetchall()
            # 修改执行标志
            excute_sql_flag_str = 'sql执行成功'
        except pyodbc.Error as e:
            print(f"SQL Error: {e}")
        finally:
            # 确保关闭游标和连接,先关闭游标再关闭连接
            DatabaseCursor.close()
            DatabaseConnection.close()
            # 返回执行标志和数据
            return excute_sql_flag_str,len(rows),rows

# 插入表
def insert_table(insert_sql_str,data_list):
    # 获得数据库连接和游标
    DatabaseConnection, DatabaseCursor = database_connection.get_database_connection_cursor()
    # sql语句执行标志
    excute_sql_flag_str = 'sql执行失败'
    if DatabaseConnection and DatabaseCursor:
        try:
            # 启用快速批量执行模式
            DatabaseCursor.fast_executemany = True
            # 执行SQL语句
            DatabaseCursor.executemany(insert_sql_str,data_list)
            # 提交事务
            DatabaseConnection.commit()
            # 修改执行标志
            excute_sql_flag_str = 'sql执行成功'
        except pyodbc.Error as e:
            print(f"SQL Error: {e}")
            # 发生错误时回滚事务
            DatabaseConnection.rollback()
        finally:
            # 确保关闭游标和连接,先关闭游标再关闭连接
            DatabaseCursor.close()
            DatabaseConnection.close()
            # 返回执行标志
            return excute_sql_flag_str,len(data_list)

# 更新表
def update_table(update_sql_str,data_list):
    # 获得数据库连接和游标
    DatabaseConnection, DatabaseCursor = database_connection.get_database_connection_cursor()
    # sql语句执行标志
    excute_sql_flag_str = 'sql执行失败'
    if DatabaseConnection and DatabaseCursor:
        try:
            # 设置为快速批量执行模式
            DatabaseCursor.fast_executemany = True
            # 执行SQL语句
            DatabaseCursor.executemany(update_sql_str,data_list)
            # 提交事务
            DatabaseConnection.commit()
            # 修改执行标志
            excute_sql_flag_str = 'sql执行成功'
        except pyodbc.Error as e:
            print(f"SQL Error: {e}")
            # 发生错误时回滚事务
            DatabaseConnection.rollback()
        finally:
            # 确保关闭游标和连接,先关闭游标再关闭连接
            DatabaseCursor.close()
            DatabaseConnection.close()
            # 返回执行标志
            return excute_sql_flag_str,len(data_list)
        
# 删除数据
def delete_table(delete_sql_str,data_list):
    # 获得数据库连接和游标
    DatabaseConnection, DatabaseCursor = database_connection.get_database_connection_cursor()
    # sql语句执行标志
    excute_sql_flag_str = 'sql执行失败'
    if DatabaseConnection and DatabaseCursor:
        try:
            # 设置为快速批量执行模式
            DatabaseCursor.fast_executemany = True
            # 执行SQL语句,批量执行不可以获得被执行的数据条数
            DatabaseCursor.executemany(delete_sql_str,data_list)
            # 提交事务
            DatabaseConnection.commit()
            # 修改执行标志
            excute_sql_flag_str = 'sql执行成功'
        except pyodbc.Error as e:
            print(f"SQL Error: {e}")
            # 发生错误时回滚事务
            DatabaseConnection.rollback()
        finally:
            # 确保关闭游标和连接,先关闭游标再关闭连接
            DatabaseCursor.close()
            DatabaseConnection.close()
            # 返回执行标志
            return excute_sql_flag_str,len(data_list)