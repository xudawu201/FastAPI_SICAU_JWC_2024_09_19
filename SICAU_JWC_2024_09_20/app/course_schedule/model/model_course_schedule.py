'''
Author: xudawu
Date: 2024-11-26 15:05:03
LastEditors: xudawu
LastEditTime: 2024-11-29 10:45:17
'''
# 课程类
class Course:
    def __init__(self, id_int,course_id,name_str, week_study_hour, theoretical_study_hour,experimental_study_hour,total_study_hour,
                 self_study_hour,CourseTeacher_list,schedule_course_type_str,course_type_str,course_system_str,
                 theoretical_selectable_student_num_int,selected_student_num_int,room_type_str,campus_area_str,
                 teaching_class_id_int,teacher_study_hour_list,
                 ):
        self.id_int = id_int
        # 课程编号
        self.course_id = course_id
        self.name_str = name_str
        # 周学时
        self.week_study_hour = week_study_hour
        # 理论课总学时
        self.theoretical_study_hour = theoretical_study_hour
        # 实验课总学时
        self.experimental_study_hour = experimental_study_hour
        # 总学时
        self.total_study_hour = total_study_hour
        # 自修(自学)学时
        self.self_study_hour = self_study_hour
        self.CourseTeacher_list = CourseTeacher_list
        # 排课类别
        self.schedule_course_type_str = schedule_course_type_str
        # 课程性质
        self.course_type_str = course_type_str
        # 数据库列名为课程体系，内容如慕课、通识必修、专业方向课
        self.course_system_str = course_system_str
        # 理论可选学生人数
        self.theoretical_selectable_student_num_int = theoretical_selectable_student_num_int
        # 已选学生人数
        self.selected_student_num_int = selected_student_num_int
        # 教室类别
        self.room_type_str = room_type_str
        # 校区
        self.campus_area_str = campus_area_str
        # 教学班编号
        self.teaching_class_id_int = teaching_class_id_int
        # 教师学时列表
        self.teacher_study_hour_list = teacher_study_hour_list
        # 优先级
        self.priority_float = 1
        
# 教师类
class Teacher:
    def __init__(self, name_str,id_int,unavailable_timeslot_list=[]):
        self.name_str = name_str
        self.id_int = id_int
        # 不可用的时间列表
        self.unavailable_timeslot_list = unavailable_timeslot_list if unavailable_timeslot_list else []
# 学生类
class Student:
    def __init__(self, id_int,student_id_str,name_str,campus_area_str,enroll_campus_area_str,semester_str,
                 new_class_str,new_major_str,new_grade_str,EnrolledCoursesList=[],TimeSlotList=[]):
        self.id_int = id_int
        self.student_id_str = student_id_str
        self.name_str = name_str
        # 新校区
        self.campus_area_str = campus_area_str
        # 选课校区
        self.enroll_campus_area_str = enroll_campus_area_str
        # 学期
        self.semester_str = semester_str
        # 新班级
        self.new_class_str = new_class_str
        # 新专业
        self.new_major_str = new_major_str
        # 新年级
        self.new_grade_str = new_grade_str
        # 记录学生的选课列表
        self.EnrolledCoursesList = EnrolledCoursesList
        # 记录学生的上课时间段
        self.TimeSlotList = TimeSlotList

    # 选课方法
    def enroll_Course(self, Course):
        self.EnrolledCoursesList.append(Course)

# 时间类
class TimeSlot:
    def __init__(self, week_time_str, day_time_str,slot_time_str):
        # 周时间
        self.week_time_str = week_time_str
        # 天时间
        self.day_time_str = day_time_str
        # 时段时间
        self.slot_time_str = slot_time_str


# 教室类
class Room:
    def __init__(self, room_id_int,campus_area_str,teaching_building_str,room_name_str,room_type_str,specific_room_type_str,capacity_int,):
        self.id_int = room_id_int
        # 校区
        self.campus_area_str = campus_area_str
        # 教学楼
        self.teaching_building_str = teaching_building_str
        self.room_name_str = room_name_str
        # 教室类型（如实验室）
        self.room_type_str = room_type_str
        # 详细教室类型（如实训室1）
        self.specific_room_type_str = specific_room_type_str
        self.capacity_int = capacity_int