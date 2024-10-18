'''
Author: xudawu
Date: 2024-10-17 11:50:08
LastEditors: xudawu
LastEditTime: 2024-10-18 15:16:11
'''
# from app.model import user
# from app.database import database_connection
# import crud
# import pyodbc

# a=user.User(id=1,username='xudawu',password='123',flag='1')
# print(a)

# 查询用户
def get_user(select_sql_str):
    rows = crud.select_table(select_sql_str)
    return rows

# 增加
def insert_user(insert_sql_str,data_list):
    crud.insert_table(insert_sql_str,data_list)

if __name__ == '__main__':
    # 引入文件目录设置
    import sys
    import os
    # 添加项目文件根目录到系统路径
    module_path = os.path.abspath('SCAU_JWC_2024_09_20')
    sys.path.append(module_path)

    from app.model import user
    from app.database import database_connection
    import crud
    import pyodbc

    a=user.User(id=1,username='xudawu',password='123',flag='1')
    print(a)

    # 查询测试
    select_sql_str ='select * from user_2024_10_16'

    rows = get_user(select_sql_str)
    for row in rows:
        print(row)

    # 插入测试
    name_str = 'test'
    password_str = '123'
    flag_str = '中文测试'
    data_list = [
        (name_str,
        password_str,
        flag_str
        ),
    ]
    insert_sql_str =  'INSERT INTO user_2024_10_16(name, password,flag) VALUES (?,?,?)'
    insert_user(insert_sql_str,data_list)
    
    # 查询测试
    select_sql_str ='select * from user_2024_10_16'

    rows = get_user(select_sql_str)
    for row in rows:
        print(row)