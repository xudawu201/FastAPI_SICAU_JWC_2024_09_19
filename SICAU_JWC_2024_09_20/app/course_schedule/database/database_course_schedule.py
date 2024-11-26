'''
Author: xudawu
Date: 2024-10-23 16:08:45
LastEditors: xudawu
LastEditTime: 2024-11-26 17:36:09
'''
# from database import database_connection

# DatabaseConnection,DatabaseCursor = database_connection.get_database_connection_cursor()

from service import crud


# 获得所有数据
def select_table_data_database(select_sql_str,):
    # 执行sql语句,返回执行标志和执行数据
    excute_sql_flag_str,excute_count_int,rows = crud.select_table(select_sql_str)
    return excute_sql_flag_str,excute_count_int,rows


if __name__ == '__main__':
    # 引入文件目录设置
    import sys
    import os
    # 添加项目文件根目录到系统路径
    module_path = os.path.abspath('')
    sys.path.append(module_path)

    from service import crud

    # 课程、教师、学生
    # 构造sql语句参数
    table_name_str = "开课任务"
    select_column_name_str='学期'
    semeste_name_str = "2024-2025-1"
    schedule_course_type_str = '混教'
    # 构造sql语句
    select_sql_str =f"select * from {table_name_str} where {select_column_name_str} = '{semeste_name_str}' and 排课类别 = '{schedule_course_type_str}'"
    excute_sql_flag_str,excute_count_int,rows = select_table_data_database(select_sql_str)

    print("执行结果：",excute_sql_flag_str)
    print("执行条数：",excute_count_int)
    print("执行数据：",rows[0])

    # 理论课教室、实践课教室
    # table_name_str = "教室"
    # # 构造sql语句
    # select_sql_str =f"select * from {table_name_str}"
    # excute_sql_flag_str,excute_count_int,rows = select_table_data_database(select_sql_str)

    # print("执行结果：",excute_sql_flag_str)
    # print("执行条数：",excute_count_int)
    # print("执行数据：",rows[0])
    # index = 0
    # for row in rows:
    #     index += 1
    #     print(index,":",row)

    # 课程限制条件
    # table_name_str = "开课限制课程"
    # select_column_name_str='学期'
    # semeste_name_str = "2024-2025-1"
    # # 构造sql语句
    # select_sql_str =f"select * from {table_name_str} where {select_column_name_str} = '{semeste_name_str}'"
    # excute_sql_flag_str,excute_count_int,rows = select_table_data_database(select_sql_str)

    # print("执行结果：",excute_sql_flag_str)
    # print("执行条数：",excute_count_int)
    # print("执行数据：",rows[0])
    # index = 0
    # for row in rows:
    #     index += 1
    #     print(index,":",row)
