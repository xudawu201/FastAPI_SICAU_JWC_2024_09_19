'''
Author: xudawu
Date: 2024-11-26 15:02:14
LastEditors: xudawu
LastEditTime: 2024-11-29 11:33:21
'''
import time

from app.course_schedule.database import database_course_schedule
from app.course_schedule.model import model_course_schedule
from app import public_function

# 初始化教师和课程类
def initialize_teacher_course(semester_str):
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
    schedule_type1_str = "混班"
    # 构造sql语句
    select_sql_str = f"""
        select * from {table_name_str} 
        where 学期 = '{semester_str}' 
        and 排课类别 != '{schedule_type1_str}' and 课程性质 !='实践教学' and 课程体系 !='慕课' and 是否排课 ='是'
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

# 设置教师不可上课时间
def set_teacher_unavailable_timeslot(Teacher_list,semester_str):
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
    select_sql_str =f"select * from {table_name_str} where 是否排课='是'"
    excute_sql_flag_str,excute_count_int,rows = database_course_schedule.select_table_data_database(select_sql_str)

    # 初始化教室列表
    Room_list = []
    for row in rows:
        id_int = row.id
        # 校区
        campus_area_str = row.校区
        # 教学楼
        teaching_building_str = row.教学楼
        room_name_str = row.教室
        # 教室类型（如实验室）
        room_type_str = row.类别
        # 详细教室类型（如实训室1）
        specific_room_type_str = row.教室小类
        capacity_int = row.容量

        room = model_course_schedule.Room(id_int,campus_area_str,teaching_building_str,room_name_str,room_type_str,specific_room_type_str,capacity_int)
        Room_list.append(room)

    return Room_list


# 初始化学生类列表
def initialize_student(semester_str):
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
    # 连接的表
    table1_name_str = '公选课选课情况'
    table2_name_str = '开课任务'
    table3_name_str = '学生花名册'
    
    # 定义排课类别变量
    schedule_type1_str = "混班"
    # 构造sql语句
    select_sql_str =f'''
        select
            a.id,a.学号,a.选课校区,a.学期,a.课程,a.编号,
            b.课程编号,b.id as 课程id,
            c.姓名,c.新校区,c.新系别,c.新年级,c.新专业,c.新班级
        from
            {table1_name_str} as a
            inner join {table2_name_str} as b on a.编号 = b.编号
            inner join {table3_name_str} as c on a.学号 = c.学号
        where
            b.学期 = '{semester_str}'
        and b.排课类别 != '{schedule_type1_str}' 
        and b.课程性质 !='实践教学'
        and b.课程体系 !='慕课'
        and b.是否排课 ='是'

    '''
    # INNER JOIN：仅返回两表中满足条件的记录。
    # ON：定义连接条件，例如表的外键与主键匹配。

    excute_sql_flag_str,excute_count_int,rows = database_course_schedule.select_table_data_database(select_sql_str)

    # 初始化学生类列表
    Student_list = []
    # 已处理学生列表
    temp_student_list = []
    # 学生和选课对应列表
    student_course_dict = {}
    # 先测试前5000的数据
    for row in rows[:2000]:
        student_id_str = row.学号
        # 将学号作为键
        if student_id_str not in student_course_dict:
            student_course_dict[student_id_str]=[row.课程id]

        else:
            student_course_dict[student_id_str].append(row.课程id)

        # 如果是新学号
        if student_id_str not in temp_student_list:
            # 更新已处理学生列表
            temp_student_list.append(student_id_str)

            id_int = row.id
            name_str = row.姓名
            # 校区
            campus_area_str = row.新校区
            # 选课校区
            enroll_campus_area_str = row.选课校区
            # 学期
            semester_str = row.学期
            # 新班级
            new_class_str = row.新班级
            # 新专业
            new_major_str = row.新专业
            # 新年级
            new_grade_str = row.新年级

            # 记录学生的选课列表
            EnrolledCoursesList = []
            # 记录学生的上课时间段
            TimeSlotList = []
            
            student = model_course_schedule.Student(id_int,student_id_str,name_str,campus_area_str,enroll_campus_area_str,semester_str,
                    new_class_str,new_major_str,new_grade_str,EnrolledCoursesList,TimeSlotList)

            # 添加学生选课列表
            Student_list.append(student)

    return student_course_dict,Student_list

# 设置学生选课
def set_student_enroll_course(Student_list,Course_list,student_course_dict):
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
    
    # 优化学生选课函数，降低执行时间复杂度O(a+b+c)
    # 预处理课程字典，加速查找,字典推导式的结构为{表达式 循环结构}
    Course_dict = {course.id_int: course for course in Course_list}

    # count_int=1
    # 遍历学生列表
    for Student in Student_list:
        # 获取该学生的选课ID列表,get(Student.student_id_str,[])设置未找到的默认值为空列表而不是None
        student_courses_list = student_course_dict.get(Student.student_id_str,[])
        # 将选课ID转为课程对象，直接添加
        for course_id in student_courses_list:
            # print(count_int,Student.student_id_str,course_id)
            # count_int+=1
            # 优化：使用字典查找，避免嵌套循环，降低时间复杂度
            Course = Course_dict.get(course_id)
            if Course:
                Student.enroll_Course(Course)
    
    # 原地返回学生列表
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
    from app import public_function

    # 上课时间初始化
    print('初始上课时间类列表开始')
    start_time = time.time()

    # 定义周、天和时间段
    week_range = range(1, 3)
    # day_range = ['1', '2', '3', '4', '5','6','7']
    day_range = ['1', '2']
    # slot_time_range =['1','2','3','4','5']
    slot_time_range =['1','2']
    # 初始化上课时间列表
    TimeSlot_list = initialize_time(week_range,day_range,slot_time_range)

    time_used = public_function.get_time_used(start_time)
    print('初始上课时间列表完成,用时:', time_used)

    print('上课时间数量:',len(TimeSlot_list))

    for TimeSlot in TimeSlot_list:
        print(TimeSlot.week_time_str, TimeSlot.day_time_str, TimeSlot.slot_time_str)
        break

    # 初始化教室类列表
    print('初始化教室类列表开始')
    start_time = time.time()

    Room_list = initialize_room()

    time_used = public_function.get_time_used(start_time)
    print('初始化教室类列表完成,用时:', time_used)

    print('教室数量:',len(Room_list))

    for room in Room_list:
        print(room.id_int, room.campus_area_str, room.room_name_str, room.room_type_str, room.specific_room_type_str, room.capacity_int)
        break
    
    # 指定学期
    semester_str = '2024-2025-1'

    # 初始化教师和课程类列表
    print('初始化教师和课程类列表开始')
    start_time = time.time()

    Teacher_list,Course_list = initialize_teacher_course(semester_str)

    time_used = public_function.get_time_used(start_time)
    print('初始化教师和课程类列表完成,用时:', time_used)

    print('课程人数:',len(Course_list))
    print('教师人数:',len(Teacher_list))

    for Teacher in Teacher_list:

        if Teacher.id_int == '14933':
            print(Teacher.id_int, Teacher.name_str, Teacher.unavailable_timeslot_list)
            break

    # 设置教师上课限制时间

    print('设置教师上课限制时间开始')
    start_time = time.time()

    Teacher_list = set_teacher_unavailable_timeslot(Teacher_list,semester_str)

    time_used = public_function.get_time_used(start_time)
    print('设置教师上课限制时间完成,用时:', time_used)

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
    print('初始化学生类列表开始')
    start_time = time.time()

    student_course_dict,Student_list = initialize_student(semester_str)

    time_used = public_function.get_time_used(start_time)
    print('初始化学生类列表完成,用时:', time_used)

    print('学生人数:',len(student_course_dict))

    for Student in Student_list:
        print(
            Student.id_int,Student.student_id_str,Student.name_str, Student.campus_area_str,Student.enroll_campus_area_str, Student.semester_str,
            Student.new_class_str, Student.new_major_str, Student.new_grade_str, 
            Student.EnrolledCoursesList, Student.TimeSlotList,
        )
        break

    # 设置学生选课
    print('设置学生选课列表开始')
    start_time = time.time()

    Student_list = set_student_enroll_course(Student_list,Course_list,student_course_dict)

    time_used = public_function.get_time_used(start_time)
    print('设置学生选课列表完成,用时:', time_used)

    for Student in Student_list:
        print(
            Student.id_int,Student.student_id_str,Student.name_str, Student.campus_area_str,Student.enroll_campus_area_str, Student.semester_str,
            Student.new_class_str, Student.new_major_str, Student.new_grade_str, 
            Student.EnrolledCoursesList, Student.TimeSlotList,
        )
        break
    