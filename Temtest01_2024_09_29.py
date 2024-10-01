'''
Author: xudawu
Date: 2024-09-29 17:54:42
LastEditors: xudawu
LastEditTime: 2024-09-30 09:30:29
'''
import sqlalchemy


# 声明表结构
metadata = sqlalchemy.MetaData()
employees = sqlalchemy.Table('student', metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('name', sqlalchemy.String),
)

# 连接数据库
engine = sqlalchemy.create_engine('postgresql+psycopg2://postgres:123@localhost/test_2024_09_29')
metadata.create_all(engine)

select_statement = employees.select()
with engine.connect() as connection:
    result_set = connection.execute(select_statement)
    for row in result_set:
        print(row,row._get_by_key_impl_mapping('name'))
        print(row[1],row.name)