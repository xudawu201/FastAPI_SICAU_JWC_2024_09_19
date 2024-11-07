'''
Author: xudawu
Date: 2024-10-23 16:08:45
LastEditors: xudawu
LastEditTime: 2024-11-07 14:49:54
'''
from service import crud

# 获得所有数据
def get_score_database(class_name_str,course_type_str,semester_str):
    # 构造sql语句
    select_sql_str =f"select 学号,成绩 from 成绩 where 班级 = '{class_name_str}' and 课程性质 = '{course_type_str}' and 学期 = '{semester_str}'"
    # 执行sql语句,返回执行标志和执行数据
    excute_sql_flag_str,excute_count_int,rows = crud.select_table(select_sql_str)
    return excute_sql_flag_str,excute_count_int,rows