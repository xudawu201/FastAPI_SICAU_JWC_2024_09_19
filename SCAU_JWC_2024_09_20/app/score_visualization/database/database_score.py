'''
Author: xudawu
Date: 2024-10-23 16:08:45
LastEditors: xudawu
LastEditTime: 2024-10-25 14:12:06
'''
from service import crud

# 获得所有数据
def get_score_database(class_name_str,course_type_str,semester_str):
    # 构造sql语句
    select_sql_str =f"select * from 成绩 where 班级 = '{class_name_str}' and 课程性质 = '{course_type_str}' and 学期 = '{semester_str}'"
    # 执行sql语句,返回执行标志和执行数据
    excute_sql_flag_str,excute_count_int,rows = crud.select_table(select_sql_str)
    return excute_sql_flag_str,excute_count_int,rows

# 获得班级对应的学院
def get_class_college_by_class_name(class_name_str):
    '''
    数据格式要求：
    class_name_str:
        班级名称,字符串类型
    返回数据：
        学院和班级,列表类型,二维列表,列表内的列表为学院和班级
    '''
    select_sql_str = f"select distinct 学院,班级 from 成绩分班 where 班级 = '{class_name_str}'"
    # 执行sql语句,返回执行标志和执行数据
    excute_sql_flag_str,excute_count_int,rows = crud.select_table(select_sql_str)
    return excute_sql_flag_str,excute_count_int,rows

# 获得班级对应的班主任
def get_class_teacher_by_class_name(class_name_str):
    '''
    数据格式要求：
    class_name_str:
        班级名称,字符串类型
    返回数据：
        学院和班级,列表类型,二维列表,列表内的列表为学院和班级
    '''
    select_sql_str = f"select distinct 班主任,班级 from 班级 where 班级 = '{class_name_str}'"
    # 执行sql语句,返回执行标志和执行数据
    excute_sql_flag_str,excute_count_int,rows = crud.select_table(select_sql_str)
    return excute_sql_flag_str,excute_count_int,rows

# 获得所有学院
def get_all_college_class():
    '''
    数据格式要求：
    class_name_str:
        班级名称,字符串类型
    返回数据：
        学院和班级,列表类型,二维列表,列表内的列表为学院和班级
    '''
    select_sql_str = f"select distinct 学院,班级 from 成绩分班"
    # 执行sql语句,返回执行标志和执行数据
    excute_sql_flag_str,excute_count_int,rows = crud.select_table(select_sql_str)
    return excute_sql_flag_str,excute_count_int,rows


# 获得班级有成绩的所有学期
def get_all_semester_by_class(class_name_str):
    '''
    数据格式要求：
    class_name_str:
        班级名称,字符串类型
    返回数据：
        学院和班级,列表类型,1维列表,列表内的元素为学期
    '''
    select_sql_str = f"select distinct 学期 from 成绩 where 班级 = '{class_name_str}'"
    # 执行sql语句,返回执行标志和执行数据
    excute_sql_flag_str,excute_count_int,rows = crud.select_table(select_sql_str)
    return excute_sql_flag_str,excute_count_int,rows

# 获得成绩表中有成绩的班级列表
def get_all_have_score_class_list():
    '''
    数据格式要求：
    student_id_str:
        学生学号,字符串类型
    row_list:
        行数据列表,列表类型，每一行是一个类对象
        一个对象包含成绩信息,学期和班级信息应当固定为特定的一个学期和特定班级,本函数不区分学期和班级，只区分学号
    预期的row_list为:
    '''
    select_sql_str = f"select distinct 班级 from 成绩"
    # 执行sql语句,返回执行标志和执行数据
    excute_sql_flag_str,excute_count_int,rows = crud.select_table(select_sql_str)
    return excute_sql_flag_str,excute_count_int,rows

# 获得班级有的课程类型名称列表
def get_all_course_type_by_class(class_name_str):
    '''
    数据格式要求：
    class_name_str:
        班级名称,字符串类型
    返回数据：
        学院和班级,列表类型,1维列表,列表内的元素为学期
    '''
    select_sql_str = f"select distinct 课程性质 from 成绩 where 班级 = '{class_name_str}'"
    # 执行sql语句,返回执行标志和执行数据
    excute_sql_flag_str,excute_count_int,rows = crud.select_table(select_sql_str)
    return excute_sql_flag_str,excute_count_int,rows