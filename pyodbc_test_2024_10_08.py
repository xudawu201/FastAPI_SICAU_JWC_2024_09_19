'''
Author: xudawu
Date: 2024-10-08 11:23:17
LastEditors: xudawu
LastEditTime: 2024-11-20 17:35:03
'''
import pyodbc

# DRIVER:驱动名称,SERVER:服务器名称,DATABASE:数据库名称,UID:用户名,PWD:密码
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=JWC_SCAU_2024_10_08;UID=sa;PWD=123')
# pyodbc使用微软的官方驱动ODBC driver对于中文的兼容性好，不需要再额外使用字符编码设置
# 创建游标对象
cursor = cnxn.cursor()

# 执行SQL语句
select_sql_str ='select * from Student_2024_10_08'
cursor.execute(select_sql_str)
print(cursor)
row = cursor.fetchone()
print(row)

cursor.execute(select_sql_str)
row = cursor.fetchone()
# 使用索引访问列数据
print('name:', row[1])
# 使用列名访问列数据
print('name:', row.name)

# 遍历所有行数据
print('遍历所有行数据')
cursor.execute(select_sql_str)
# 当数据为空时fetchone()会返回None
while True:
    row = cursor.fetchone()
    if row==None:
        break
    print('name:', row.name)

# 直接访问所有数据
cursor.execute(select_sql_str)
rows = cursor.fetchall()
print('直接访问所有数据')
print(rows)

# 插入数据
insert_sql_str = "INSERT INTO Student_2024_10_08(name) VALUES ('中文测试7')"
cursor.execute(insert_sql_str)
cnxn.commit()

# 直接访问所有数据
cursor.execute(select_sql_str)
rows = cursor.fetchall()
print('直接访问所有数据')
print(rows)

# 关闭游标和连接
cursor.close()
cnxn.close()
