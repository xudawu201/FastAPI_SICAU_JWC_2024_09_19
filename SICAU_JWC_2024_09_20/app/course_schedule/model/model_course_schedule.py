'''
Author: xudawu
Date: 2024-11-26 15:05:03
LastEditors: xudawu
LastEditTime: 2024-11-26 17:17:13
'''
# 课程类
class Course:
    def __init__(self, name_str, CourseTeacher, duration_float, priority_float=1):
        self.name_str = name_str
        self.CourseTeacher = CourseTeacher
        self.duration_float = duration_float
        self.priority_float = priority_float

# 教师类
class Teacher:
    def __init__(self, name_str,id_int,unavailable_timeslot_list=[]):
        self.name_str = name_str
        self.id_int = id_int
        # 不可用的时间列表
        self.unavailable_timeslot_list = unavailable_timeslot_list if unavailable_timeslot_list else []
# 学生类
class Student:
    def __init__(self, name_str):
        self.name_str = name_str
        self.enrolled_courses_list = []
        # 记录学生的上课时间段
        self.time_slots_list = []

    # 选课方法
    def enroll(self, course):
        self.enrolled_courses_list.append(course)

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
    def __init__(self, room_id_int,teaching_area_str,teaching_building_str,room_name_str,first_type_str,second_type_str,capacity_int):
        self.id_int = room_id_int
        # 教学区
        self.teaching_area_str = teaching_area_str
        # 教学楼
        self.teaching_building_str = teaching_building_str
        self.room_name_str = room_name_str
        # 教室类型（如实验室）
        self.first_type_str = first_type_str
        # 详细教室类型（如实训室1）
        self.second_type_str = second_type_str
        self.capacity_int = capacity_int