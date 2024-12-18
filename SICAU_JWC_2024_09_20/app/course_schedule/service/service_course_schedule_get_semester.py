'''
Author: xudawu
Date: 2024-12-18 16:41:55
LastEditors: xudawu
LastEditTime: 2024-12-18 17:05:07
'''
from app.course_schedule.database import database_course_schedule

# 初始化教室
def initialize_semester():
    '''
    输入数据格式要求：
    返回数据：
    Room_list:
        教室类型列表
        示例：
        [
            <app.course_schedule.model.model_course_schedule.Room object at 0x0000000005FCE570>,
            <app.course_schedule.model.model_course_schedule.Room object at 0x000000000608B620>
        ]
    '''
    # 理论课教室、实践课教室
    table_name_str = "开课任务"
    # 构造sql语句
    select_sql_str =f"select distinct 学期 from {table_name_str} where 是否排课='是'"
    excute_sql_flag_str,excute_count_int,rows = database_course_schedule.select_table_data_database(select_sql_str)

    # 初始化学期字典
    semester_dict = {'semester_list':[],'message_list':[]}
    for row in rows:
        # 跳过空值
        if row.学期 is None:
            continue
        
        # 添加数据
        semester_dict['semester_list'].append(row.学期)
    
    # 返回字典
    return semester_dict



if __name__ == '__main__':
    # 引入文件目录设置
    import sys
    import os
    # 添加项目文件根目录到系统路径
    module_path = os.path.abspath('')
    sys.path.append(module_path)

    from app.course_schedule.database import database_course_schedule


    semester_dict = initialize_semester()