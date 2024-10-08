'''
Author: xudawu
Date: 2024-09-30 09:36:46
LastEditors: xudawu
LastEditTime: 2024-10-08 11:15:07
'''
import sqlalchemy


# 声明表结构
metadata = sqlalchemy.MetaData()
Student = sqlalchemy.Table('student', metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('name', sqlalchemy.String),
)

# 连接数据库
# 数据库类型://用户名:密码@主机名:端口号/数据库名
# DataBaseEngine = sqlalchemy.create_engine('postgresql://postgres:123@localhost:5432/test_2024_09_29')
DataBaseEngine = sqlalchemy.create_engine('mssql://sa:123@127.0.0.1:1433/JWC_SCAU_2024_10_08')
# metadata.create_all(DataBaseEngine)
    
# 使用ORM查询数据
# select_statement = Student.select()
# with DataBaseEngine.connect() as DataBaseConnection:
#     result_set = DataBaseConnection.execute(select_statement)
#     for row in result_set:
#         print(row,row._get_by_key_impl_mapping('name'))
#         print(row[1],row.name)

# 使用SQL语句查询数据
with DataBaseEngine.connect() as DataBaseConnection:
    select_sql_str = 'SELECT * FROM student'
    result_set = DataBaseConnection.execute(sqlalchemy.text(select_sql_str))
    for row in result_set:
        print(row,row._get_by_key_impl_mapping('name'))
        print(row[1],row.name)


# 使用SQL语句插入数据
# with DataBaseEngine.connect() as DataBaseConnection:
#     insert_sql_str = "INSERT INTO student(name) VALUES ('中文测试2')"
#     result_set = DataBaseConnection.execute(sqlalchemy.text(insert_sql_str))
#     print(result_set)
#     # 提交事务
#     DataBaseConnection.commit()

# 使用SQL语句删除数据
# with DataBaseEngine.connect() as DataBaseConnection:
#     delete_sql_str = "DELETE FROM student where id=2"
#     result_set = DataBaseConnection.execute(sqlalchemy.text(delete_sql_str))
#     print(result_set)
#     # 提交事务
#     DataBaseConnection.commit()