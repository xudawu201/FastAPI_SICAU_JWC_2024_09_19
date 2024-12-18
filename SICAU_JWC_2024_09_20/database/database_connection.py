'''
Author: xudawu
Date: 2024-10-15 10:14:52
LastEditors: xudawu
LastEditTime: 2024-12-18 17:51:52
'''
import pyodbc

# DRIVER:驱动名称,SERVER:服务器url,DATABASE:数据库名称,UID:用户名,PWD:密码,Encrypt=no不使用加密连接
# database_url = 'DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=SICAU_JWC;UID=sa;PWD=sicau_jwc_sqlserver123;Encrypt=no;TrustServerCertificate=yes'
# 使用sqlserver本地调试数据库
database_url = 'DRIVER={ODBC Driver 18 for SQL Server};SERVER=127.0.0.1;PORT=1433;DATABASE=jxgl_all;UID=sa;PWD=sicau_jwc_sqlserver123;Encrypt=no'

# 使用sqlserver容器部署数据库
# database_url = 'DRIVER={ODBC Driver 18 for SQL Server};SERVER=172.18.0.1;PORT=1433;DATABASE=jxgl_all;UID=sa;PWD=sicau_jwc_sqlserver123;Encrypt=no'

# 使用信教中心sqlserver容器部署数据库
# database_url = 'DRIVER={ODBC Driver 18 for SQL Server};SERVER=10.99.84.138;PORT=32120;DATABASE=jxgl_all;UID=sa;PWD=sicau_jwc_sqlserver123;Encrypt=no'

# 使用postgres本地调试数据库
# database_url = 'DRIVER={PostgreSQL Unicode(x64)};SERVER=localhost;PORT=5432;DATABASE=SICAU_JWC;UID=postgres;PWD=docker_postgres;'

# 使用postgres部署容器数据库
# database_url = 'DRIVER={PostgreSQL Unicode(x64)};SERVER=postgres17;PORT=5432;DATABASE=SICAU_JWC;UID=postgres;PWD=docker_postgres;'

# 使用mysql本地调试数据库
# database_url = 'DRIVER={MySQL ODBC 9.1 Unicode Driver};SERVER=localhost;PORT=3306;DATABASE=SICAU_JWC;UID=root;PWD=sicau_jwc_mysql123;'

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
            select_sql_str = 'select * from 班级'
            # select_sql_str = 'select * from Student_2024_10_08'
            DatabaseCursor.execute(select_sql_str)
            row = DatabaseCursor.fetchone()
            print(row)
            # print(row.专业)
            print('- '*20)
            
            # rows = DatabaseCursor.fetchall()
            # for row in rows:
            #     print(row)
            #     print('- '*20)
            
        except pyodbc.Error as e:
            print(f"SQL Error: {e}")
        finally:
            # 确保关闭游标和连接,先关闭游标再关闭连接
            DatabaseCursor.close()
            DatabaseConnection.close()