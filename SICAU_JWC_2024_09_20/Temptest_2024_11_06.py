import pyodbc

database_url = 'DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;PORT=1433;DATABASE=jxgl_all;UID=sa;PWD=sicau_jwc_sqlserver123;Encrypt=no;TrustServerCertificate=yes'
connection = pyodbc.connect(database_url)

# 执行查询
cursor = connection.cursor()
select_sql_str = 'select * from 班级'
cursor.execute(select_sql_str)
result = cursor.fetchone()
print(result)
