'''
Author: xudawu
Date: 2024-11-26 15:02:14
LastEditors: xudawu
LastEditTime: 2024-11-26 18:00:25
'''

# 初始化教师
def initialize_teacher():
    '''
    输入数据格式要求：
    返回数据：
    Teacher_list:
        教师类列表
        示例：
        [
            <app.course_schedule.model.model_course_schedule.Teacher object at 0x0000000005FCE570>,
            <app.course_schedule.model.model_course_schedule.Teacher object at 0x000000000608B620>
        ]
    '''
    # 理论课教室、实践课教室
    table_name_str = "开课任务"
    # 学期
    semester_str = "2024-2025-1"
    schedule_type1_str = "混教"
    schedule_type2_str = '选课'
    schedule_type3_str = '实验'
    # 构造sql语句
    select_sql_str = f"""
        select * from {table_name_str} 
        where 学期 = '{semester_str}' 
        and (
            排课类别 = '{schedule_type1_str}' 
            or 排课类别 = '{schedule_type2_str}' 
            or 排课类别 = '{schedule_type3_str}'
        )
    """
    excute_sql_flag_str,excute_count_int,rows = database_course_schedule.select_table_data_database(select_sql_str)

    # 初始化教师列表
    Teacher_list = []
    for row in rows:
        id_int = row.id
        # 教学区
        teaching_area_str = row.教学区
        # 教学楼
        teaching_building_str = row.教学楼
        room_name_str = row.教室
        # 教室类型（如实验室）
        first_type_str = row.类别
        # 详细教室类型（如实训室1）
        second_type_str = row.教室小类
        capacity_int = row.容量

        # 教师姓名、id、不可上课时间列表
        teacher = model_course_schedule.Teacher(f'teacher{i}',i,unavailable_timeslot_list)
        Teacher_list.append(teacher)

    return Teacher_list

# 初始化上课时间
def initialize_time(week_range,day_range,slot_time_range):
    '''
    输入数据格式要求：
    返回数据：
    TimeSlot_list:
        时间类列表
        示例：
        [
            <app.course_schedule.model.model_course_schedule.TimeSlot object at 0x0000000005FCE570>,
            <app.course_schedule.model.model_course_schedule.TimeSlot object at 0x000000000608B620>
        ]
    '''
    # 初始化列表
    TimeSlot_list = []

    # 生成时间段
    for week in week_range:
        for day in day_range:
            for slot_time in slot_time_range:
                timeslot = model_course_schedule.TimeSlot(week, day, slot_time)
                TimeSlot_list.append(timeslot)

    return TimeSlot_list

# 初始化教室
def initialize_room():
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
    table_name_str = "教室"
    # 构造sql语句
    select_sql_str =f"select * from {table_name_str}"
    excute_sql_flag_str,excute_count_int,rows = database_course_schedule.select_table_data_database(select_sql_str)

    # 初始化教室列表
    Room_list = []
    for row in rows:
        id_int = row.id
        # 教学区
        teaching_area_str = row.教学区
        # 教学楼
        teaching_building_str = row.教学楼
        room_name_str = row.教室
        # 教室类型（如实验室）
        first_type_str = row.类别
        # 详细教室类型（如实训室1）
        second_type_str = row.教室小类
        capacity_int = row.容量

        room = model_course_schedule.Room(id_int,teaching_area_str,teaching_building_str,room_name_str,first_type_str,second_type_str,capacity_int)
        Room_list.append(room)

    return Room_list

if __name__ == '__main__':
    # 引入文件目录设置
    import sys
    import os
    # 添加项目文件根目录到系统路径
    module_path = os.path.abspath('')
    sys.path.append(module_path)

    from app.course_schedule.database import database_course_schedule
    from app.course_schedule.model import model_course_schedule

    # 上课时间初始化
    # 定义周、天和时间段
    week_range = range(1, 3)
    # day_range = ['星期1', '星期2', '星期3', '星期4', '星期5','星期6','星期7']
    day_range = ['星期1', '星期2']
    # slot_time_range =['第1讲','第2讲','第3讲','第4讲','第5讲']
    slot_time_range =['第1讲','第2讲']
    # 初始化上课时间列表
    TimeSlot_list = initialize_time(week_range,day_range,slot_time_range)

    for TimeSlot in TimeSlot_list:
        print(TimeSlot.week_time_str, TimeSlot.day_time_str, TimeSlot.slot_time_str)
        break

    # 初始化教室列表
    Room_list = initialize_room()

    for room in Room_list:
        print(room.id_int, room.teaching_building_str, room.room_name_str, room.first_type_str, room.second_type_str, room.capacity_int)
        break
    
    # 初始化教师列表
    Teacher_list = initialize_teacher()

