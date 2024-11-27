'''
Author: xudawu
Date: 2024-11-26 15:02:14
LastEditors: xudawu
LastEditTime: 2024-11-27 18:00:00
'''

# 初始化教师和课程类
def initialize_teacher_course():
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
    Course_list:
        课程类列表
        示例：
        [
            <app.course_schedule.model.model_course_schedule.Course object at 0x0000000005FCE570>,
            <app.course_schedule.model.model_course_schedule.Course object at 0x000000000608B620>
        ]
    '''

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
        and 课程性质 !='实践教学' and 课程体系 !='慕课'
    """

    excute_sql_flag_str,excute_count_int,rows = database_course_schedule.select_table_data_database(select_sql_str)

    # 初始化教师列表
    Teacher_list = []
    # 初始化课程列表
    Course_list = []
    # 初始化临时教师列表
    temp_teacher_list = []

    for row in rows:
        
        # 初始化临时教师列表
        TempTeacherList = []
        # 初始化临时教师学时列表
        TempTeacherStudyHourList = []

        # 教师1
        teacher_name_str = row.教师
        # 教师工号
        teacher_id_str = row.教师工号

        TempTeacherList.append(model_course_schedule.Teacher(teacher_name_str,teacher_id_str,[]))
        TempTeacherStudyHourList.append(row.教师学时)

        if teacher_id_str not in temp_teacher_list:
            unavailable_timeslot_list=[]
            # 教师姓名、id、不可上课时间列表
            teacher = model_course_schedule.Teacher(teacher_name_str,teacher_id_str,unavailable_timeslot_list)
            Teacher_list.append(teacher)

            # 更新已处理教师列表
            temp_teacher_list.append(teacher_id_str)

        
        # 教师2
        teacher_name_str = row.教师1
        if teacher_name_str != '无':
            # 教师工号
            teacher_id_str = row.教师1工号
            
            TempTeacherList.append(model_course_schedule.Teacher(teacher_name_str,teacher_id_str,[]))
            TempTeacherStudyHourList.append(row.教师1学时)

            if teacher_id_str not in temp_teacher_list:
                teacher = model_course_schedule.Teacher(teacher_name_str,teacher_id_str,[])
                Teacher_list.append(teacher)

                # 更新已处理教师列表
                temp_teacher_list.append(teacher_id_str)

        # 教师3
        teacher_name_str = row.教师2
        if teacher_name_str != '无':
            # 教师工号
            teacher_id_str = row.教师2工号

            TempTeacherList.append(model_course_schedule.Teacher(teacher_name_str,teacher_id_str,[]))
            TempTeacherStudyHourList.append(row.教师2学时)

            if teacher_id_str not in temp_teacher_list:
                teacher = model_course_schedule.Teacher(teacher_name_str,teacher_id_str,[])
                Teacher_list.append(teacher)

                # 更新已处理教师列表
                temp_teacher_list.append(teacher_id_str)

        # 教师4
        teacher_name_str = row.教师3
        if teacher_name_str != '无':
            # 教师工号
            teacher_id_str = row.教师3工号

            TempTeacherList.append(model_course_schedule.Teacher(teacher_name_str,teacher_id_str,[]))
            TempTeacherStudyHourList.append(row.教师3学时)

            if teacher_id_str not in temp_teacher_list:
                teacher = model_course_schedule.Teacher(teacher_name_str,teacher_id_str,[])
                Teacher_list.append(teacher)

                # 更新已处理教师列表
                temp_teacher_list.append(teacher_id_str)

        # 课程列表
        id_int = row.id
        # 课程编号
        course_id = row.课程编号
        name_str = row.课程
        # 周学时
        week_study_hour = row.周学时
        # 理论课总学时
        theoretical_study_hour = row.理论学时
        # 实验课总学时
        experimental_study_hour = row.实验学时
        # 总学时
        total_study_hour = row.总学时
        # 自修(自学)学时
        self_study_hour = row.自修
        CourseTeacher_list = TempTeacherList
        # 排课类别
        schedule_course_type_str = row.排课类别
        # 课程性质
        course_type_str = row.课程性质
        # 数据库列名为课程体系，内容如慕课、通识必修、专业方向课
        course_system_str = row.课程体系
        # 理论可选学生人数
        theoretical_selectable_student_num_int = row.人数
        # 已选学生人数
        selected_student_num_int = row.已选人数
        # 教室类别
        room_type_str = row.教室类别
        # 校区
        campus_area_str = row.校区
        # 教学班编号
        teaching_class_id_int = row.编号
        # 教师学时列表
        teacher_study_hour_list = TempTeacherStudyHourList

        course = model_course_schedule.Course(
            id_int,course_id,name_str, week_study_hour, theoretical_study_hour,experimental_study_hour,total_study_hour,
            self_study_hour,CourseTeacher_list,schedule_course_type_str,course_type_str,course_system_str,
            theoretical_selectable_student_num_int,selected_student_num_int,room_type_str,campus_area_str,
            teaching_class_id_int,teacher_study_hour_list,
        )
        Course_list.append(course)

    return Teacher_list,Course_list

# 初始化教师不可上课时间
def initialize_teacher_unavailable_timeslot(Teacher_list):
    '''
    输入数据格式要求：
    返回数据：
    Teacher_list:
        教师类列表
        示例：
        [
            <app.course_schedule.model.model_course_schedule.Teacher object at 0x0000000005FCE570>,
            <app.course_schedule.model.model_course_schedule.Teacher object at 0x000000000608B620>,
        ]
    '''
    # 理论课教室、实践课教室
    table_name_str = "开课限制教师"
    # 学期
    semester_str = "2024-2025-1"
    # 构造sql语句
    select_sql_str = f"""
        select * from {table_name_str} 
        where 学期 = '{semester_str}' 
    """
    excute_sql_flag_str,excute_count_int,rows = database_course_schedule.select_table_data_database(select_sql_str)

    for row in rows:
        # 教师1
        teacher_id_str = row.教师编号
        # 遍历教师列表
        for Teacher in Teacher_list:
            if Teacher.id_int == teacher_id_str:
                # 不可上课时间
                temp_unavailable_timeslot_str = row.限制时间
                # 将不可上课时间转换为列表
                temp_unavailable_timeslot_list = temp_unavailable_timeslot_str.split(',')
                # 删除指定元素
                remove_str='0'
                while remove_str in temp_unavailable_timeslot_list:
                    temp_unavailable_timeslot_list.remove(remove_str)
                
                # 初始化不可上课时间列表
                unavailable_timeslot_list=[]

                # 分割不可上课时间
                for unavailable_timeslot in temp_unavailable_timeslot_list:
                    day_str,time_str = unavailable_timeslot.split('-')
                    # 使用0来代表所有周
                    timeslot = model_course_schedule.TimeSlot(0, day_str, time_str)
                    unavailable_timeslot_list.append(timeslot)

                # 添加不可上课时间
                Teacher.unavailable_timeslot_list = unavailable_timeslot_list

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


# 初始化学生类列表
def initialize_student():
    '''
    输入数据格式要求：
    返回数据：
    Student_list:
        学生类列表
        示例：
        [
            <app.course_schedule.model.model_course_schedule.Student object at 0x0000000005FCE570>,
            <app.course_schedule.model.model_course_schedule.Student object at 0x000000000608B620>
        ]
    '''
    # 学生表
    table_name_str = "学生"
    # 构造sql语句
    select_sql_str =f'''
        select
            a.id,a.学号,a.姓名,a.课程编号,a.编号,a.课程,a.上课时间,a.班级,a.优选专业
            b.记分,a.时间,a.锁定,a.调班前编号,b.课程,b.学分,a.课程性质,b.任课单位,b.学期,
            b.上课时间,b.教师,b.课程组别,b.教师1,b.人数,b.已选人数,b.周次1,b.教室,c.姓名,
            c.年级,c.系别,c.专业,c.班级,b.分组编号,b.优选专业,b.在读情况,b.考查成绩比例,b.实验成绩比例,
            b.平时成绩比例,c.新系别,c.新专业,c.新班级,a.考务,c.性别,a.缓考申请时间,a.经办人,a.阅次,a.选购教材,
            b.课程性质 AS 开课课程性质,c.校区,a.选课校区,c.新校区,b.状态,c.个人电话,a.课程类别,b.课程体系,
            b.培养层次,b.考核方法,a.操作号,c.理论编号,a.记载教职,a.序列变动,b.排课类别,c.民族,
            b.安排考试,b.教研工号,b.课程班级,c.照片名,c.数字分组编号,b.总学时,b.理论学时,b.实验学时,
            a.排考否,a.毕业生
        from
            公选课选课情况 as a
            inner join 开课任务 as b on a.编号 = b.编号
            inner join 学生花名册 as c on a.学号 = c.学号;
    '''

    select_sql1_str =f'''
        select
            a.id,a.学号,b.班级,c.姓名
        from
            公选课选课情况 as a
            inner join 开课任务 as b on a.编号 = b.编号
            inner join 学生花名册 as c on a.学号 = c.学号;
    '''
    # INNER JOIN：仅返回两表中满足条件的记录。
    # ON：定义连接条件，例如表的外键与主键匹配。

    excute_sql_flag_str,excute_count_int,rows = database_course_schedule.select_table_data_database(select_sql1_str)

    # 初始化学生类列表
    Student_list = []
    for row in rows:
        id_int = row.id

    return Student_list


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
    # day_range = ['1', '2', '3', '4', '5','6','7']
    day_range = ['1', '2']
    # slot_time_range =['1','2','3','4','5']
    slot_time_range =['1','2']
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
    
    # 初始化教师和课程类列表
    Teacher_list,Course_list = initialize_teacher_course()

    for Teacher in Teacher_list:
        if Teacher.id_int == '14933':
            print(Teacher.id_int, Teacher.name_str, Teacher.unavailable_timeslot_list)
            break

    # 初始化教师上课限制时间
    initialize_teacher_unavailable_timeslot(Teacher_list)

    for Teacher in Teacher_list:
        if Teacher.unavailable_timeslot_list != []:
            print(Teacher.id_int, Teacher.name_str, Teacher.unavailable_timeslot_list)
            for unavailable_timeslot in Teacher.unavailable_timeslot_list:
                print(unavailable_timeslot.week_time_str, unavailable_timeslot.day_time_str, unavailable_timeslot.slot_time_str)
            break
    
    for Course in Course_list:
        print(
            Course.id_int, Course.course_id, Course.name_str, Course.week_study_hour, Course.theoretical_study_hour,
            Course.experimental_study_hour, Course.total_study_hour, Course.self_study_hour, 
            Course.CourseTeacher_list, Course.schedule_course_type_str, Course.course_type_str, Course.course_system_str,
            Course.theoretical_selectable_student_num_int, Course.selected_student_num_int, Course.room_type_str,
            Course.campus_area_str, Course.teaching_class_id_int,Course.teacher_study_hour_list
        )
        break

    # 初始化学生类列表
    Student_list = initialize_student()