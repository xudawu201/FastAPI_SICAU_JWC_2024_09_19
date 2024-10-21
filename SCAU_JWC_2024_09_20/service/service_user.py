'''
Author: xudawu
Date: 2024-10-17 11:50:08
LastEditors: xudawu
LastEditTime: 2024-10-21 14:36:16
'''
from model import user
from service import crud

# a=user.User(id=1,username='xudawu',password='123',flag='1')
# print(a)

# 查询用户
def get_user(select_sql_str):
    # 执行sql语句,返回执行标志和执行数据
    excute_sql_flag_str,excute_count_int,rows = crud.select_table(select_sql_str)
    return excute_sql_flag_str,excute_count_int,rows

# 增加
def insert_user(insert_sql_str,data_list):
    # 执行sql语句,返回执行标志和执行条数
    excute_sql_flag_str,excute_count_int = crud.insert_table(insert_sql_str,data_list)
    return excute_sql_flag_str,excute_count_int

# 修改
def update_user(update_sql_str,data_list):
    # 执行sql语句,返回执行标志和执行条数
    excute_sql_flag_str,excute_count_int = crud.update_table(update_sql_str,data_list)
    return excute_sql_flag_str,excute_count_int

# 删除
def delete_user(delete_sql_str,data_list):
    # 执行sql语句,返回执行标志和执行条数
    excute_sql_flag_str,excute_count_int = crud.delete_table(delete_sql_str,data_list)
    return excute_sql_flag_str,excute_count_int

# 获得用户名和密码
def get_user_by_employee_no(employee_no_int):
    # 执行sql语句,返回执行标志和执行数据
    # sql查询外层双引号，内层单引号，实现字符串嵌套
    select_sql_str =f"select * from 用户 where 教师编号='{employee_no_int}'"
    excute_sql_flag_str,excute_count_int,rows = get_user(select_sql_str)
    return rows

if __name__ == '__main__':
    # 引入文件目录设置
    import sys
    import os
    # 添加项目文件根目录到系统路径
    module_path = os.path.abspath('SCAU_JWC_2024_09_20')
    sys.path.append(module_path)

    from model import user
    from database import database_connection
    import crud
    import pyodbc

    a=user.User(id=1,username='xudawu',password='123',flag='1')
    print(a)

    # id_int = 1
    # # 查询测试
    # select_sql_str =f'select * from user_2024_10_16 where id={id_int}'

    # excute_sql_flag_str,excute_count_int,rows = get_user(select_sql_str)
    # print(excute_sql_flag_str,excute_count_int,rows)

    # 字符串嵌套外层双引号，内层单引号
    rows = get_user_by_employee_no('73294')
    print(rows)

    # 插入测试
    # name_str = 'test'
    # password_str = '123'
    # flag_str = '中文测试'
    # data_list = [(name_str,password_str,flag_str),]
    # insert_sql_str =  'INSERT INTO user_2024_10_16(name, password,flag) VALUES (?,?,?)'
    # excute_sql_flag_str,excute_count_int =insert_user(insert_sql_str,data_list)
    
    # print(excute_sql_flag_str,excute_count_int)

    # 修改测试,sql中的字符串要加双引号
    # hash_password = '$pbkdf2-sha256$29000$aw3BuNf6H8MYQ8j5X0tJ6Q$8nX0D7HpWq34L.GctNkUgqx9iI1DQWbBW4MMlqMj4jo'
    # name_str = '徐大武'
    # update_sql_str = 'UPDATE 用户 SET 哈希密码 =? WHERE 姓名 =?'
    # data_list = [(hash_password,name_str),]
    # excute_sql_flag_str,excute_count_int = update_user(update_sql_str,data_list)
    # print(excute_sql_flag_str,excute_count_int)
    
    # 删除测试
    # id_int = 2
    # delete_sql_str = 'DELETE FROM user_2024_10_16 WHERE id =?'
    # data_list = [(id_int,),]
    # excute_sql_flag_str,excute_count_int = delete_user(delete_sql_str,data_list)
    # print(excute_sql_flag_str,excute_count_int)