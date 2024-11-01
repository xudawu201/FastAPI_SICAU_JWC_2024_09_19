'''
Author: xudawu
Date: 2024-10-15 10:14:52
LastEditors: xudawu
LastEditTime: 2024-11-01 16:21:42
'''
import pyodbc

# DRIVER:驱动名称,SERVER:服务器url,DATABASE:数据库名称,UID:用户名,PWD:密码
# database_url = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=SCAU_JWC_2024_11_01;UID=sa;PWD=scau_jwc_sqlserver123'
# 教务处数据库
database_url = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=jxgl_all;UID=sa;PWD=scau_jwc_sqlserver123'

# 连接到数据库
def get_database_connection_cursor():
    try:
        # 获得数据库连接对象
        DatabaseConnection = pyodbc.connect(database_url)
        # pyodbc使用微软的官方驱动ODBC driver对于中文的兼容性好，不需要再额外使用字符编码设置
        # 获得游标对象
        DatabaseCursor = DatabaseConnection.cursor()

        return DatabaseConnection,DatabaseCursor
    except pyodbc.Error as e:
        print(f"Error: {e}")
        return None
    
if __name__ == "__main__":
    # 获取数据库连接和游标
    DatabaseConnection, DatabaseCursor = get_database_connection_cursor()
    if DatabaseConnection and DatabaseCursor:
        try:
            # 执行SQL语句
            select_sql_str = 'select * from aa财务'
            # select_sql_str = 'select * from Student_2024_10_08'
            DatabaseCursor.execute(select_sql_str)
            row = DatabaseCursor.fetchone()
            print(row)
            print(row.姓名)
            # print('- '*20)
            # print(row.cursor_description)
            # print('- '*20)
            # print(row.cursor_description[0][0])
            # print(row.cursor_description[0][1])
            # print('- '*20)
            # print(row[0])
            # column_name_str = row.cursor_description[1][0]
            # print(column_name_str)
            # print(row.password)
        except pyodbc.Error as e:
            print(f"SQL Error: {e}")
        finally:
            # 确保关闭游标和连接,先关闭游标再关闭连接
            DatabaseCursor.close()
            DatabaseConnection.close()