'''
Author: xudawu
Date: 2024-11-12 08:22:18
LastEditors: xudawu
LastEditTime: 2024-11-12 10:19:08
'''
from service import crud
import passlib.context

# 获得用户信息
def get_user(table_name_str):
    '''
    数据格式要求：
    class_name_str:
        班级名称,字符串类型
    返回数据：
        sql执行标志,执行数据条数,执行数据
    '''
    select_sql_str = f"select * from {table_name_str}"
    # 执行sql语句,返回执行标志和执行数据
    excute_sql_flag_str,excute_count_int,rows = crud.select_table(select_sql_str)
    return excute_sql_flag_str,excute_count_int,rows

# 设置哈希密码
def set_hash_password(password_str):
    # 创建密码上下文对象,使用bcrypt算法
    pwd_context = passlib.context.CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
    # 哈希密码
    hashed_password = pwd_context.hash(password_str)
    return hashed_password

# 修改密码
def update_password(table_name_str,employee_no_int,hashed_password_str):
    # 使用参数化查询来避免 SQL 注入和处理特殊字符
    update_sql_str = f"update {table_name_str} set 哈希密码 = ? where 教师编号 = ?"
    data_list = [
        (hashed_password_str, employee_no_int)
        ]
    excute_sql_flag_str = crud.update_table(update_sql_str,data_list)
    return excute_sql_flag_str

# 修改所有用户密码为身份证号后六位
def update_all_password():
    excute_sql_flag_str,excute_count_int,rows = get_user('用户')
    excuted_int = 0
    for user in rows:
        # print(user.身份证号[12:])
        # print(user.教师编号)
        # print(user.哈希密码)
        try:
            # 获得哈希密码
            hashed_password_str = set_hash_password(user.身份证号[12:])

            # 修改密码
            excute_sql_flag_str = update_password('用户',user.教师编号,hashed_password_str)

            excuted_int += 1
            print(f'{excuted_int}/{excute_count_int},{user.教师编号},{excute_sql_flag_str},{hashed_password_str}')
        except Exception as e:
            print(f'{excuted_int}/{excute_count_int},{user.教师编号},{excute_sql_flag_str},{e}')
            continue

# 修改单个用户的密码
def update_single_password(employee_no_int,password_str):
    # 获得哈希密码
    hashed_password_str = set_hash_password(password_str)

    # 修改密码
    excute_sql_flag_str = update_password('用户',employee_no_int,hashed_password_str)

    print(f'{employee_no_int},{excute_sql_flag_str},{hashed_password_str}')

if __name__ == '__main__':

    # 修改徐大武密码为test
    employee_no_int = '73294'
    password_str = 'test'
    # update_single_password(employee_no_int,password_str)