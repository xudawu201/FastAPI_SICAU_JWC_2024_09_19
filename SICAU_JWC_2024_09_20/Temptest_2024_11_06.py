'''
Author: xudawu
Date: 2024-11-06 16:28:23
LastEditors: xudawu
LastEditTime: 2024-11-07 14:15:26
'''
import pyodbc

# print(pyodbc.drivers())

database_url = 'DRIVER={MySQL ODBC 9.1 Unicode Driver};SERVER=localhost;PORT=3306;DATABASE=SICAU_JWC;UID=root;PWD=sicau_jwc_mysql123;'

# database_url = 'DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;PORT=1433;DATABASE=jxgl_all;UID=sa;PWD=sicau_jwc_sqlserver123;Encrypt=no;TrustServerCertificate=yes'
connection = pyodbc.connect(database_url)

# 执行查询
cursor = connection.cursor()
select_sql_str = 'select * from 班级'
cursor.execute(select_sql_str)
result = cursor.fetchone()
print(result)
