'''
Author: xudawu
Date: 2024-09-18 16:39:56
LastEditors: xudawu
LastEditTime: 2024-12-04 16:15:43
'''
# 遗传算法随机库
import random
import time
import copy

# fastapi相关
from fastapi import APIRouter, Request,WebSocket
import asyncio

# # 引入模板模块
from template import TemplatesJinja2CourseSchedule
from app.course_schedule.service import service_course_schedule
from app.course_schedule.model import model_course_schedule
from app import public_function

# 全局超参数

router = APIRouter()

# 遗传算法类
class GeneticAlgorithm:
    def __init__(self, Course_list, TimeSlot_list, Room_list, Student_list):
        self.Course_list = Course_list
        self.TimeSlot_list = TimeSlot_list
        self.Room_list = Room_list
        self.Student_list = Student_list
        # 初始化排课类,用于随机选课
        self.Schedule_list = []
        # 初始化安排索引,键为四元组(周,天,讲,教室id)),值为Schedule类,用字典查找Schedule类优化性能
        self.ScheduleIndex_dict = {}
        # 根据校区和教室类型生成不同的课程字典,键是一个二元组 (校区, 教室类型),值为对应课程
        self.CourseByCampusAndType_dict = {}
        # 学生冲突信息
        self.conflict_info_list = []

        # 工作日
        self.workday_day_time_dict = {1, 2, 3, 4, 5}
        # 周末
        self.weekend_day_time_dict = {6}
        # 实验排课起始讲
        self.experiment_start_slot_dict = {1,3,5}
        # 被继承的实验课起始讲
        self.experiment_inherit_start_slot_dict = {1,3}
        # 要继承的实验课的讲
        self.experiment_inherit_slot_dict = {2,4}
        # 实验课算排两次的讲
        self.experiment_course_count_double_slot_dict = {5}
        # 实验室名字
        self.experiment_room_name_str = '实验室'
        # 排课类别名字
        self.schedule_course_type_str = '实验'
        
        # 初始化已删除没有匹配课程的教室列表
        self.NoMatchAreaOrTypeCourseRoom_list = []
        # 初始化已删除没有匹配课程已选人数的教室列表
        self.NoMatchCapacityCourseRoom_list = []

        # 以教师id和上课周为键，上课次数为值
        self.teacher_assigned_dict = {}
        # 初始化安排理论课程字典
        self.theory_course_assigned_dict = {}
        # 初始化安排实验课程字典
        self.experiment_course_assigned_dict = {}

    # 获得容量匹配的课程列表
    def get_capacity_match_course_list(self, CurRoom,AvailableCourse_list):
        # 根据教室容量筛选符合条件的课程
        CapacityAvailableCourse_list = [
            Course for Course in AvailableCourse_list
            if Course.selected_student_num_int <= CurRoom.capacity_int
        ]
        return CapacityAvailableCourse_list

    # 根据安排索引安排课程
    def set_schedule_course(self, Schedule,ChoiceCourse):
        Schedule.Course = ChoiceCourse
        
    # 设置2、4讲的实验课继承1、3讲的实验课
    def initialize_schedule_experiment_inherit(self,CurSchedule,ChoiceCourse):
        # 排第二讲,如果属于1、3讲
        if CurSchedule.TimeSlot.slot_time_int in self.experiment_inherit_start_slot_dict:
            # 查找下一讲的时间段
            next_slot_key = (CurSchedule.TimeSlot.week_time_int, CurSchedule.TimeSlot.day_time_int, CurSchedule.TimeSlot.slot_time_int + 1,CurSchedule.Room.id_int)
            NextSlotSchedule = self.ScheduleIndex_dict.get(next_slot_key, None)
            if NextSlotSchedule!=None:
                # 安排课程
                self.set_schedule_course(NextSlotSchedule,ChoiceCourse)

    # 排理论课
    def initialize_schedule_theory(self, CurSchedule,ChoiceCourse):
        # 只在工作日排理论课
        if CurSchedule.TimeSlot.day_time_int in self.workday_day_time_dict:
            # 更新课程安排
            self.set_schedule_course(CurSchedule,ChoiceCourse)
    # 排实验课
    def initialize_schedule_experiment(self,CurSchedule,ChoiceCourse):
        self.set_schedule_course(CurSchedule,ChoiceCourse)

    # 获得教室对应的课程
    def get_schedule(self,CurTimeSlot,CurRoom):
        # 根据教室的校区和类型获取可用课程列表
        AvailableCourse_list = self.CourseByCampusAndType_dict.get((CurRoom.campus_area_str, CurRoom.room_type_str), [])
        
        # 遍历可用课程
        if AvailableCourse_list==[]:
            print(f"没有找到符合类型条件的课程:{CurTimeSlot.week_time_int}{CurTimeSlot.day_time_int}{CurTimeSlot.slot_time_int}没有校区为{CurRoom.campus_area_str}，教室类型为{CurRoom.room_type_str}的课程")
            # 记录教室
            self.NoMatchAreaOrTypeCourseRoom_list.append(CurRoom)
            return None
        
        # 根据教室容量筛选符合条件的课程
        CapacityAvailableCourse_list = self.get_capacity_match_course_list(CurRoom,AvailableCourse_list)
        if CapacityAvailableCourse_list==[]:
            print(f"没有找到符合容量条件的课程: 时间{CurTimeSlot.week_time_int}{CurTimeSlot.day_time_int}{CurTimeSlot.slot_time_int},{CurRoom.room_name_str} ({CurRoom.capacity_int}人) ")
            # 记录教室
            self.NoMatchCapacityCourseRoom_list.append(CurRoom)
            return None

        # 直接随机选择一门课程
        ChoiceCourse = random.choice(CapacityAvailableCourse_list)
        return ChoiceCourse

    # 初始化基因,去掉不能排课的教室
    def initialize(self):

        # 初始化排课安排列表和初始化安排索引
        for CurTimeSlot in self.TimeSlot_list:
            for CurRoom in self.Room_list:
                # 初始化排课安排列表
                schedule = model_course_schedule.Schedule(CurTimeSlot, CurRoom, None)
                self.Schedule_list.append(schedule)

                # 初始化安排索引
                key = (CurTimeSlot.week_time_int, CurTimeSlot.day_time_int, CurTimeSlot.slot_time_int,CurRoom.id_int)
                self.ScheduleIndex_dict[key] = schedule

        # 初始化字典结构以存储每个校区和教室类型的教室列表
        for Course in self.Course_list:
            # 键是一个二元组 (校区, 教室类型)
            key = (Course.campus_area_str, Course.room_type_str)
            if key not in self.CourseByCampusAndType_dict:
                self.CourseByCampusAndType_dict[key] = []
            self.CourseByCampusAndType_dict[key].append(Course)

        # 排课
        for CurSchedule in self.Schedule_list:
            # 获得教室对应的课程
            ChoiceCourse = self.get_schedule(CurSchedule.TimeSlot,CurSchedule.Room)
            # 如果有匹配的课
            if ChoiceCourse!=None:
                # 根据课程类别在对应排课
                schedule_course_type_str = ChoiceCourse.schedule_course_type_str
                # 排实验课,只排1、3、5讲,2、4讲直接继承上一讲
                if schedule_course_type_str==self.schedule_course_type_str:
                    # 1、3、5讲直接排
                    if CurTimeSlot.slot_time_int in self.experiment_start_slot_dict:
                        self.initialize_schedule_experiment(CurSchedule,ChoiceCourse)
                    # 如果是1、3讲,2、4讲继承
                    if CurTimeSlot.slot_time_int in self.experiment_inherit_start_slot_dict:
                        # 2、4讲继承
                        self.initialize_schedule_experiment_inherit(CurSchedule,ChoiceCourse)
                # 排理论课
                else:
                    self.initialize_schedule_theory(CurSchedule,ChoiceCourse)
        # 教室库删除没有类型和容量匹配的教室
        self.Room_list = [Room for Room in self.Room_list if Room not in self.NoMatchAreaOrTypeCourseRoom_list and Room not in self.NoMatchCapacityCourseRoom_list]

        Room_list = copy.deepcopy(self.Room_list)
        return Room_list

    # 基因变异操作
    def mutate(self):
        # 随机选择一个时间段和教室组合
        ChoiceSchedule = random.choice(self.Schedule_list)

        # 随机找一个可以替换的课程
        # 现在有匹配的课,根据现有的课类别排课
        if ChoiceSchedule.Course!=None:
            # 根据课程类别在对应排课
            schedule_course_type_str = ChoiceSchedule.Course.schedule_course_type_str
            # 获得教室对应的课程,随机选一门课
            ChoiceCourse = self.get_schedule(ChoiceSchedule.TimeSlot,ChoiceSchedule.Room)
            # 如果有课再排
            if ChoiceCourse!=None:
                # 排实验课
                if schedule_course_type_str==self.schedule_course_type_str:
                    # 只在1、3、5讲排
                    if ChoiceSchedule.TimeSlot.slot_time_int in self.experiment_start_slot_dict:
                        self.initialize_schedule_experiment(ChoiceSchedule,ChoiceCourse)
                    # 如果是1、3讲,2、4讲继承
                    if ChoiceSchedule.TimeSlot.slot_time_int in self.experiment_inherit_start_slot_dict:
                        # 2、4讲继承
                        self.initialize_schedule_experiment_inherit(ChoiceSchedule,ChoiceCourse)
                # 排理论课
                else:
                    self.initialize_schedule_theory(ChoiceSchedule,ChoiceCourse)
        # 现在没有匹配的课,根据选的课类别排课
        else:
            # 获得教室对应的课程,随机选一门课
            ChoiceCourse = self.get_schedule(ChoiceSchedule.TimeSlot,ChoiceSchedule.Room)
            # 如果有课再排
            if ChoiceCourse!=None:
                # 根据课程类别在对应排课
                schedule_course_type_str = ChoiceCourse.schedule_course_type_str
                # 排实验课
                if schedule_course_type_str==self.schedule_course_type_str:
                    # 只在1、3、5讲排
                    if ChoiceSchedule.TimeSlot.slot_time_int in self.experiment_start_slot_dict:
                        self.initialize_schedule_experiment(ChoiceSchedule,ChoiceCourse)
                    # 如果是1、3讲,2、4讲继承
                    if ChoiceSchedule.TimeSlot.slot_time_int in self.experiment_inherit_start_slot_dict:
                        # 2、4讲继承
                        self.initialize_schedule_experiment_inherit(ChoiceSchedule,ChoiceCourse)
                # 排理论课
                else:
                    self.initialize_schedule_theory(ChoiceSchedule,ChoiceCourse)

    # 批量处理2、4讲的实验课继承于1、3讲
    def batch_initialize_schedule_experiment_inherit(self,Schedule_list):
        for CurSchedule in Schedule_list:
            if CurSchedule.Course!=None:
                # 处理实验课
                if CurSchedule.Course.schedule_course_type_str==self.schedule_course_type_str:
                    # 如果为可继承的起始讲
                    if CurSchedule.TimeSlot.slot_time_int in self.experiment_inherit_start_slot_dict:
                        # 2、4讲继承
                        self.initialize_schedule_experiment_inherit(CurSchedule,CurSchedule.Course)
        return Schedule_list

    # 基因交叉操作
    def crossover(self, OtherParent):
        # 随机选择交叉基因的起点
        crossover_index_int = random.randint(0, len(self.Schedule_list) - 1)
        # 初始化两个子代的基因
        child1_schedule_list = []
        child2_schedule_list = []

        # 迭代交换基因
        for index, CurSchedule in enumerate(self.Schedule_list):
            # 子代1交叉基因起点之前的基因来自本个体,子代2的基因来自其他个体
            if index <= crossover_index_int:
                child1_schedule_list.append(self.Schedule_list[index])
                child2_schedule_list.append(OtherParent.Schedule_list[index])
            else:
                # 子代1交叉基因起点之后的基因来自其他个体,子代2的基因来自本个体
                child1_schedule_list.append(OtherParent.Schedule_list[index])
                child2_schedule_list.append(self.Schedule_list[index])

        # 初始化两个子代类的基因
        Child1Schedule = GeneticAlgorithm(self.Course_list, self.TimeSlot_list, self.Room_list, self.Student_list)
        Child2Schedule = GeneticAlgorithm(self.Course_list, self.TimeSlot_list, self.Room_list, self.Student_list)

        # 批量处理2、4讲的实验课
        child1_schedule_list = self.batch_initialize_schedule_experiment_inherit(child1_schedule_list)
        child2_schedule_list = self.batch_initialize_schedule_experiment_inherit(child2_schedule_list)

        # 赋予子代基因
        Child1Schedule.Schedule_list = child1_schedule_list
        Child2Schedule.Schedule_list = child2_schedule_list

        # 返回两个新子代基因
        return Child1Schedule, Child2Schedule
    
    # 学生适应度
    def student_fitness(self,CurTimeSlot,CurCourse):
        fitness_float = 0
        # 学生不能同时上两门及以上课程,进行冲突检测
        for CurStudent in self.Student_list:
            # 如果学生选了此门课程
            if CurCourse in CurStudent.EnrolledCoursesList:
                # 如果学生上课时间段中有此上课时间
                if CurTimeSlot in CurStudent.TimeSlotList:
                    # 有冲突大幅降低适应度
                    fitness_float -= 6
                    # 记录冲突信息
                    self.conflict_info_list.append((CurStudent.id_int, CurCourse.id_int, CurTimeSlot))

                # 更新学生的时间段表,增加此上课时间到学生的上课时间表中
                else:
                    CurStudent.TimeSlotList.append(CurTimeSlot)

        return fitness_float

    # 计算适应度
    def fitness(self):
        fitness_float = 0
        course_time_dict = {}

        # 初始化学生冲突时间表为空列表
        for CurStudent in self.Student_list:
            CurStudent.TimeSlotList = []

        # 初始化已处理教师列表
        teacher_processed_id_list = []
        # 每个教师和课程被安排的次数初始化为0
        for CurCourse in self.Course_list:
            # 初始化教师被安排的次数,有多个教师,分别处理
            for CurTeacher in CurCourse.CourseTeacher_list:
                if CurTeacher.id_int in teacher_processed_id_list : continue
                teacher_processed_id_list.append(CurTeacher.id_int)
                # 初始化已处理周数
                teacher_week_time_list=[]
                for CurTimeSlot in self.TimeSlot_list:
                    if CurTimeSlot.week_time_int not in teacher_week_time_list:
                        # 更新已处理周数
                        teacher_week_time_list.append(CurTimeSlot.week_time_int)
                        key = (CurTimeSlot.week_time_int,CurTeacher.id_int)
                        self.teacher_assigned_dict[key] = 0

            # 初始化已处理周数
            course_week_time_list=[]
            for CurTimeSlot in self.TimeSlot_list:
                if CurTimeSlot.week_time_int not in course_week_time_list:
                    # 更新已处理周数
                    course_week_time_list.append(CurTimeSlot.week_time_int)
                    key = (CurTimeSlot.week_time_int,CurCourse.id_int)
                    # 排课类别为实验的课程,初始化课程被安排的次数
                    if CurCourse.schedule_course_type_str == self.schedule_course_type_str:
                        self.experiment_course_assigned_dict[key] = 0
                    # 理论课的课程,初始化课程被安排的次数
                    else:
                        self.theory_course_assigned_dict[key] = 0
                        
        # 计算适应度
        for CurSchedule in self.Schedule_list:
            # 如果当前时段有课程安排,则进行判断
            if CurSchedule.Course is not None:
                # 同一课程同一时间不能安排在多个教室,同一时间同一课程名代表有冲突
                # 在安排中则代表有冲突
                if (CurSchedule.TimeSlot, CurSchedule.Room) in course_time_dict:
                    fitness_float -= 6
                else:
                    # 没有在安排表中，记录此次安排
                    course_time_dict[(CurSchedule.TimeSlot, CurSchedule.Room)] = CurSchedule.Course
                    
                # 安排此课,适应度分值加上优先级分值
                fitness_float += CurSchedule.Course.priority_float
                # 统计教师被安排的次数
                for CurTeacher in CurSchedule.Course.CourseTeacher_list:
                    key=(CurSchedule.TimeSlot.week_time_int,CurTeacher.id_int)
                    # 如果是实验课并且安排在第5讲,算排了两次课
                    if CurSchedule.Course.schedule_course_type_str == self.schedule_course_type_str and CurSchedule.TimeSlot.slot_time_int in self.experiment_course_count_double_slot_dict:
                        self.teacher_assigned_dict[key] += 2
                    else:
                        self.teacher_assigned_dict[key] += 1
                        
                # 分别计算理论课和实验课被安排的次数
                key = (CurSchedule.TimeSlot.week_time_int,CurSchedule.Course.id_int)
                if CurSchedule.Course.schedule_course_type_str == self.schedule_course_type_str:
                    if CurSchedule.TimeSlot.slot_time_int in self.experiment_course_count_double_slot_dict:
                        self.experiment_course_assigned_dict[key] +=2
                    else:
                        self.experiment_course_assigned_dict[key] +=1
                else:
                    self.theory_course_assigned_dict[key] += 1

                # 计算学生相关适应度
                student_fitness_float = self.student_fitness(CurSchedule.TimeSlot,CurSchedule.Course)
                fitness_float += student_fitness_float

                # 如果此门课程的安排时间在教师不可以上课的时间列表中，适应度大幅降低
                for CourseTeacher in CurSchedule.Course.CourseTeacher_list:
                    for TeacherUnavailableTimeSlot in CourseTeacher.unavailable_timeslot_list:
                        if CurSchedule.TimeSlot.day_time_int == TeacherUnavailableTimeSlot.day_time_int and CurSchedule.TimeSlot.slot_time_int == TeacherUnavailableTimeSlot.slot_time_int :
                            fitness_float -= 6

        # 理论课周排课均衡性评分
        for (week_time_int,course_id_int), course_assigned_count_int in self.theory_course_assigned_dict.items():
            # 没有排课
            if course_assigned_count_int == 0:
                fitness_float -= 5
            # 2-4次排课,即2-4周学时是合理的
            elif 2<= course_assigned_count_int <= 4:
                fitness_float += 2
            # 其他情况,直接减去排课次数的分,次数越多减的越多
            else:
                fitness_float -= course_assigned_count_int

        # 实验课周排课均衡性评分
        for (week_time_int,course_id_int), course_assigned_count_int in self.experiment_course_assigned_dict.items():
            # print((week_time_int,course_id_int), course_assigned_count_int)
            # 没有排课
            if course_assigned_count_int == 0:
                fitness_float -= 5
            # 1-2次排课,即4-8周学时是合理的
            elif 4<= course_assigned_count_int <= 8:
                fitness_float += 2
            # 其他情况,直接减去排课次数的分,次数越多减的越多
            else:
                fitness_float -= course_assigned_count_int

        # 返回适应度
        return fitness_float

    # 找到课程本周的安排的讲数
    def get_course_assigned_count(self,CurTimeSlot,CurCourse):
        # 获得key键
        key=(CurTimeSlot.week_time_int,CurCourse.id_int)
        # 处理实验课
        if CurCourse.schedule_course_type_str == self.schedule_course_type_str:
            schedule_week_count_int = self.experiment_course_assigned_dict.get(key,-1)
            return schedule_week_count_int
        # 处理理论课
        else:
            schedule_week_count_int = self.theory_course_assigned_dict.get(key,-1)
            return schedule_week_count_int
    def display(self):

        # 未安排课程字典
        unassigned_course_dict = {}
        
        '''
        CurCourse的属性有:
        duration_float =1.3930817605509733
        name_str ='class100'
        priority_float =1
        teacher_str ='teacher14'
        unavailable_timeslots_list =[]
        '''

        # 添加未安排的课程信息
        for CurCourse in self.Course_list:
            cur_course_teacher_id_str=''
            for CurTeacher in CurCourse.CourseTeacher_list:
                if CurTeacher != None:
                    cur_course_teacher_id_str+=str(CurTeacher.id_int)+','
            cur_course_str = f'course_name:{CurCourse.name_str},teacher:{cur_course_teacher_id_str},priority:{CurCourse.priority_float}'
            # 添加字典数据
            unassigned_course_dict[CurCourse.id_int]=cur_course_str
        
        # 用集合去重
        unassigned_rooms = set(self.Room_list)
        unassigned_students = set(str(Student.student_id_str) for Student in self.Student_list)

        # 初始化当前代排课信息字典
        current_generation_info_dict = {
            # 初始化当前代排课信息
            "room_assigned_course_schedule_dict": {},
            # 初始化未安排的教室和时间段
            "unassigned_time_list": [],
            # 初始化未安排的教师
            "unassigned_teacher_list": [],
            # 初始化未安排的教室
            "unassigned_room_list": [],
            # 初始化未安排的学生
            'unassigned_student_list': []
        }

        # 初始化排课索引
        schedule_index_int = 0
        # 初始化未安排时间列表
        unassigned_time_list = []
        # 初始化上课时间冲突教师列表
        schedule_conflict_time_teachers_list = []
        # 初始化上课时间冲突学生列表
        schedule_conflict_time_student_list = []
        for CurSchedule in self.Schedule_list:
            # 初始化当前排课信息
            room_course_schedule_str=''
            # 如果课程为非空,则打印课程信息
            if CurSchedule.Course is not None:
                # 初始化本门课的选课学生列表
                enrolled_course_student_name_list = []
                # 遍历学生列表
                for CurStudent in self.Student_list:
                    # 如果本门课在当前学生选课列表中,则将学生姓名加入选课学生列表
                    if CurSchedule.Course in CurStudent.EnrolledCoursesList:
                        enrolled_course_student_name_list.append(str(CurStudent.student_id_str))
                        # 从未安排列表中移除学生
                        unassigned_students.discard(str(CurStudent.student_id_str))
                enrolled_course_student_str = ", ".join(enrolled_course_student_name_list) if enrolled_course_student_name_list else "No student enrolled"

                # 初始化教师不可上课信息
                availability_str = ''
                # 检查教师是否在不可上课时间
                for CurTeacher in CurSchedule.Course.CourseTeacher_list:
                    if CurSchedule.TimeSlot in CurTeacher.unavailable_timeslot_list:
                        availability_str = "teacher unavailable during this time"
                        # 添加教师上课时间冲突表
                        schedule_conflict_time_teachers_list.append(CurTeacher.id_int)


                # 初始化学生上课时间冲突信息
                conflict_str = ""
                for (cur_student_id_int, cur_course_id_int, CurTimeSlot) in self.conflict_info_list:
                    if cur_course_id_int == CurSchedule.Course.id_int and CurTimeSlot == CurSchedule.TimeSlot:
                        conflict_str = f"{cur_course_id_int}"

                        # 添加学生上课时间冲突表
                        schedule_conflict_time_student_list.append(cur_course_id_int)
                
                # 找到教师
                teacher_id_str = ''
                for CurTeacher in CurSchedule.Course.CourseTeacher_list:
                    teacher_id_str+=str(CurTeacher.id_int)+','
                # 排课时间、教师、课程名、授课教师、课程优先级、选课学生、冲突信息、是否处于教师不可上课时间、不可上课信息
                # room_course_schedule_str = f"week:{CurSchedule.TimeSlot.week_time_int},day:{CurSchedule.TimeSlot.day_time_int},time:{CurSchedule.TimeSlot.slot_time_int} in {CurSchedule.Room.room_name_str}: {CurSchedule.Course.name_str} by {teacher_id_str} (Priority: {CurSchedule.Course.priority_float}) | Enrolled: {enrolled_course_student_str} | student_conflict:{conflict_str} | teacher_availability:{availability_str}"
                
                # 初始化处理教师不可上课时间为列表
                teatcher_unavailable_timeslot_list=[]
                for CurTeacher in CurSchedule.Course.CourseTeacher_list:
                    # 如果有不可上课时间
                    if CurTeacher.unavailable_timeslot_list != []:
                        for ThisCurTimeSlot in CurTeacher.unavailable_timeslot_list:
                            this_cur_time_slot_list=[f'week:{ThisCurTimeSlot.week_time_int},day:{ThisCurTimeSlot.day_time_int},time:{ThisCurTimeSlot.slot_time_int}']
                            teatcher_unavailable_timeslot_list.append(this_cur_time_slot_list)
                
                # 找到本周此课程安排次数(讲数)
                schedule_week_count_int = self.get_course_assigned_count(CurSchedule.TimeSlot,CurSchedule.Course)

                # 添加到字典中,使用排课安排索引作为键,值为排课信息
                current_generation_info_dict["room_assigned_course_schedule_dict"][f'schedule{schedule_index_int}']={
                    'week':CurSchedule.TimeSlot.week_time_int,'day':CurSchedule.TimeSlot.day_time_int,
                    "time":CurSchedule.TimeSlot.slot_time_int,"room":CurSchedule.Room.room_name_str,
                    "course":CurSchedule.Course.name_str,"teacher":teacher_id_str,"priority":CurSchedule.Course.priority_float,
                    "enrolled_student":enrolled_course_student_str,"conflict":conflict_str,"availability":availability_str,
                    'unavailable_timeslots_teacher':teatcher_unavailable_timeslot_list, 
                    
                    'schedule_course_type':CurSchedule.Course.schedule_course_type_str,
                    'campus_area_str':CurSchedule.Room.campus_area_str,
                    'schedule_week_count_int':schedule_week_count_int,
                    }

                # 从未安排列表中移除教室
                unassigned_rooms.discard(CurSchedule.Room)
                try:
                    # 将已排的课从未安排课中移除
                    removed_value = unassigned_course_dict.pop(CurSchedule.Course.id_int)
                except KeyError:
                    # 键不存在,则跳过
                    pass

            else:
                # 未安排教室和时间段
                unassigned_time_list.append(CurSchedule.TimeSlot)
                # room_course_schedule_str = f"week:{CurSchedule.TimeSlot.week_time_int},day:{CurSchedule.TimeSlot.day_time_int},time:{CurSchedule.TimeSlot.slot_time_int} in {CurSchedule.Room.room_name_str}: Free"
                current_generation_info_dict["room_assigned_course_schedule_dict"][f'schedule{schedule_index_int}']={
                    'week':CurSchedule.TimeSlot.week_time_int,'day':CurSchedule.TimeSlot.day_time_int,
                    "time":CurSchedule.TimeSlot.slot_time_int,"room":CurSchedule.Room.room_name_str,
                    "course":'未安排排课',"teacher":'',"priority":'',"enrolled_student":'',"conflict":'',
                    "availability":'','unavailable_timeslots_teacher':[],

                    'schedule_course_type':'',
                    'campus_area_str':CurSchedule.Room.campus_area_str,
                    'schedule_week_count_int':''
                    }
            
            # 更新排课安排索引
            schedule_index_int += 1
            # 打印排课信息
            # print(room_course_schedule_str)
        
        # 打印上课时间冲突的教师
        # 获得去重的字符串
        unique_conflict_time_teachers_list_str =list_remove_duplicate_joint(schedule_conflict_time_teachers_list)
        if unique_conflict_time_teachers_list_str == '':
            unique_conflict_time_teachers_list_str = "无"
        # 添加到字典中
        current_generation_info_dict["schedule_conflict_time_teacher"]=unique_conflict_time_teachers_list_str
        # print('unique_conflict_time_teachers_list_str:',unique_conflict_time_teachers_list_str)

        # 未安排的排课课程添加到字典中
        # 如果全部排课完成,则为空字典
        if unassigned_course_dict=={}:
            unassigned_course_dict="无"

        current_generation_info_dict["unassigned_course_dict"]=unassigned_course_dict

        # 打印上课时间冲突的学生
        # 获得去重的字符串
        unique_conflict_time_student_list_str =list_remove_duplicate_joint(schedule_conflict_time_student_list)
        if unique_conflict_time_student_list_str == '':
            unique_conflict_time_student_list_str = "无"
        # 添加到字典中
        current_generation_info_dict["schedule_conflict_time_student"]=unique_conflict_time_student_list_str
        # print('unique_conflict_time_student_list_str:',unique_conflict_time_student_list_str)

        # 打印未安排的时间段
        unique_unassigned_time_list_str =list_remove_duplicate_joint(unassigned_time_list)
        if unique_unassigned_time_list_str == '':
            unique_unassigned_time_list_str = "无"
        # 添加到字典中
        current_generation_info_dict["unassigned_time_list"]=unique_unassigned_time_list_str
        # print('unique_unassigned_time_list_str:',unique_unassigned_time_list_str)

        if unassigned_rooms:
            unassigned_room_str=''
            for CurRoom in unassigned_rooms:
                unassigned_room_str+=CurRoom.room_name_str+','
        else:
            unassigned_room_str = "无"
        # 添加到字典中
        current_generation_info_dict["unassigned_room_list"]=unassigned_room_str
        # print('unassigned_room_str:',unassigned_room_str)

        # 未安排学生
        if unassigned_students:
            unassigned_student_str = "" + ", ".join(unassigned_students)
        else:
            unassigned_student_str = "无"
        # 添加到字典中
        current_generation_info_dict["unassigned_student_list"]=unassigned_student_str
        # print('unassigned_student_str:',unassigned_student_str)

        return current_generation_info_dict

# 列表去重并拼接
def list_remove_duplicate_joint(cur_list):
    # 用集合去重
    cur_set=set(cur_list)
    # 再转为列表
    unique_list=list(cur_set)

    # 列表拼接为字符串
    unique_list_str=''
    for cur_item in unique_list:
        unique_list_str+=str(cur_item)
        unique_list_str+=','
        
    # 返回列表拼接后的字符串
    return unique_list_str

# 初始化种群
def initialize_population(Course_list, TimeSlot_list, Room_list, Student_list, population_size=100):

    # 执行一个个体初始化,修改教室列表
    # 实例化一个个体
    SingleSchedule = GeneticAlgorithm(Course_list, TimeSlot_list, Room_list, Student_list)
    # 对个体的基因进行随机初始化
    # 随机一个基因(对时间段和教室的组合随机选择一门课)
    CopyRoom_list = SingleSchedule.initialize()

    # 种群列表初始化
    Population_list = []
    # count_int=0
    for count_int in range(population_size):
        # print(f'count:{count_int+1}/{population_size},初始化单个个体开始')
        # start_time = time.time()
        # 实例化一个个体
        SingleSchedule = GeneticAlgorithm(Course_list, TimeSlot_list, CopyRoom_list, Student_list)
        # 对个体的基因进行随机初始化
        # 随机一个基因(对时间段和教室的组合随机选择一门课)
        CopyRoom2_list = SingleSchedule.initialize()

        # 将初始化后的个体加入种群列表
        Population_list.append(SingleSchedule)
        # time_used = public_function.get_time_used(start_time)
        # print('初始化单个个体完成,用时:', time_used)
    # 返回初始化的种群列表
    return Population_list

# 交叉和变异获得下一代种群
def genetic_evolution(Population_list,retention_number_int):
    
    # 计算适应度,并对种群列表进行倒序排序
    Population_list.sort(key=lambda x: x.fitness(), reverse=True)

    # 初始化下一代个体列表
    NextGeneration_list = []
    # 保留最优的部分个体
    for i in range(retention_number_int):
        NextGeneration_list.append(Population_list[i])

    # 选择和交叉,直到达到种群大小
    while len(NextGeneration_list) < len(Population_list):
        # 随机在适应度最高的部分中选择父母
        Parent1 = random.choice(Population_list[:10])
        Parent2 = random.choice(Population_list[:10])
        # 对父母基因进行交叉,得到两个子代
        Child1, Child2 = Parent1.crossover(Parent2)
        # 将两个子代加入下一代个体列表
        NextGeneration_list.append(Child1)
        NextGeneration_list.append(Child2)

    # 子代和父代有概率变异(随机变异一个基因点),这里的概率为30%
    for ChildsChedule in NextGeneration_list:
        if random.random() < 0.3:
            ChildsChedule.mutate()

    return NextGeneration_list

# 渲染前端页面的路由
@router.get("/course_schedule")
async def course_schedule(request: Request):
    return TemplatesJinja2CourseSchedule.TemplateResponse("course_schedule.html", {"request": request})

# 开始排课
@router.websocket("/ws_course_schedule")
async def ws_course_schedule(websocket: WebSocket):
  
    # 上课时间初始化
    print('初始上课时间类列表开始')
    start_time = time.time()
    # 定义周、天和时间段
    week_range = range(1, 2)
    day_range = ['1', '2', '3', '4', '5','6']
    slot_time_range =[1,2,3,4,5]
    # 初始化上课时间列表
    TimeSlot_list = service_course_schedule.initialize_time(week_range,day_range,slot_time_range)
    time_used = public_function.get_time_used(start_time)
    print('初始上课时间列表完成,用时:', time_used)
    print('上课时间数量:',len(TimeSlot_list))

    # 初始化教室类列表
    print('初始化教室类列表开始')
    start_time = time.time()
    Room_list = service_course_schedule.initialize_room()
    time_used = public_function.get_time_used(start_time)
    print('初始化教室类列表完成,用时:', time_used)
    print('教室数量:',len(Room_list))
    
    # 指定学期
    semester_str = '2024-2025-1'
    # 初始化教师和课程类列表
    print('初始化教师和课程类列表开始')
    start_time = time.time()
    Teacher_list,Course_list = service_course_schedule.initialize_teacher_course(semester_str)
    time_used = public_function.get_time_used(start_time)
    print('初始化教师和课程类列表完成,用时:', time_used)
    print('课程人数:',len(Course_list))
    print('教师人数:',len(Teacher_list))

    # 设置教师上课限制时间
    print('设置教师上课限制时间开始')
    start_time = time.time()
    Teacher_list = service_course_schedule.set_teacher_unavailable_timeslot(Teacher_list,semester_str)
    time_used = public_function.get_time_used(start_time)
    print('设置教师上课限制时间完成,用时:', time_used)

    # 初始化学生类列表
    print('初始化学生类列表开始')
    start_time = time.time()
    student_course_dict,Student_list = service_course_schedule.initialize_student(semester_str)
    time_used = public_function.get_time_used(start_time)
    print('初始化学生类列表完成,用时:', time_used)
    print('学生人数:',len(student_course_dict))

    # 设置学生选课
    print('设置学生选课列表开始')
    start_time = time.time()
    Student_list = service_course_schedule.set_student_enroll_course(Student_list,Course_list,student_course_dict)
    time_used = public_function.get_time_used(start_time)
    print('设置学生选课列表完成,用时:', time_used)
    
    # 种群大小和适应度阈值
    population_size_int = 100
    fitness_threshold_float = 50000
    # 保留最优的多少个
    retention_number_int=5

    print('排课种群初始化开始')
    start_time = time.time()
    # 获得初始化的种群
    PopulationList = initialize_population(Course_list, TimeSlot_list, Room_list, Student_list, population_size_int)
    time_used = public_function.get_time_used(start_time)
    print('排课种群初始化完成,用时:', time_used)

    # 初始化进化次数
    generation_int = 0
    # 等待接受WebSocket连接
    await websocket.accept()
    while True:
        # 交叉和变异获得下一代种群
        # 使用asyncio的to_thread方法将同步函数转换为异步函数
        # PopulationList = await asyncio.to_thread(genetic_evolution,PopulationList,retention_number_int)
        PopulationList = genetic_evolution(PopulationList,retention_number_int)

        # 获取最优个体
        BestSchedule = max(PopulationList, key=lambda x: x.fitness())
        # BestSchedule = await asyncio.to_thread(max, PopulationList, key=lambda x: x.fitness())
        # 获得最优个体的适应度
        best_fitness_float = await asyncio.to_thread(BestSchedule.fitness)
        # best_fitness_float = BestSchedule.fitness()

        # 打印当前代的最优适应度
        generation_int += 1
        # print(f"Generation {generation_int}: Best Fitness = {best_fitness_float}")
        # 获得当前代的排课信息
        # current_generation_info_dict = await asyncio.to_thread(BestSchedule.display)
        current_generation_info_dict = BestSchedule.display()
        # 获得已排课的课程数
        total_assigned_course_number = len(current_generation_info_dict['room_assigned_course_schedule_dict'].keys())
        # 字典添加代数和适应度
        current_generation_info_dict['generation_int']=generation_int
        current_generation_info_dict['fitness_float']=best_fitness_float
        current_generation_info_dict['total_assigned_course_number']=total_assigned_course_number
        # 将内容发送给前端实时显示
        await websocket.send_json({"generation": generation_int,"best_fitness":best_fitness_float,'current_generation_info_dict':current_generation_info_dict})

        # 如果达到了适应度要求，退出循环
        # if best_fitness_float >= fitness_threshold_float:
        #     break

    # print(f"best_fitness_float:{best_fitness_float},Final Best Schedule:")
    # 将内容发送给前端实时显示
    # await websocket.send_json({"generation": generation_int,"best_fitness":best_fitness_float})
    # best_schedule.display()

if __name__ == "__main__":

    # 引入文件目录设置
    import sys
    import os
    # 添加项目文件根目录到系统路径
    module_path = os.path.abspath('')
    sys.path.append(module_path)

    from app.course_schedule.service import service_course_schedule
    from app.course_schedule.model import model_course_schedule
    from app import public_function

    # 上课时间初始化
    print('初始上课时间类列表开始')
    start_time = time.time()
    # 定义周、天和时间段
    week_range = range(1, 2)
    day_range = ['1', '2', '3', '4', '5','6']
    slot_time_range =[1,2,3,4,5]
    # 初始化上课时间列表
    TimeSlot_list = service_course_schedule.initialize_time(week_range,day_range,slot_time_range)
    time_used = public_function.get_time_used(start_time)
    print('初始上课时间列表完成,用时:', time_used)
    print('上课时间数量:',len(TimeSlot_list))

    # 初始化教室类列表
    print('初始化教室类列表开始')
    start_time = time.time()
    Room_list = service_course_schedule.initialize_room()
    time_used = public_function.get_time_used(start_time)
    print('初始化教室类列表完成,用时:', time_used)
    print('教室数量:',len(Room_list))
    
    # 指定学期
    semester_str = '2024-2025-1'
    # 初始化教师和课程类列表
    print('初始化教师和课程类列表开始')
    start_time = time.time()
    Teacher_list,Course_list = service_course_schedule.initialize_teacher_course(semester_str)
    time_used = public_function.get_time_used(start_time)
    print('初始化教师和课程类列表完成,用时:', time_used)
    print('课程人数:',len(Course_list))
    print('教师人数:',len(Teacher_list))

    # 设置教师上课限制时间
    print('设置教师上课限制时间开始')
    start_time = time.time()
    Teacher_list = service_course_schedule.set_teacher_unavailable_timeslot(Teacher_list,semester_str)
    time_used = public_function.get_time_used(start_time)
    print('设置教师上课限制时间完成,用时:', time_used)

    # 初始化学生类列表
    print('初始化学生类列表开始')
    start_time = time.time()
    student_course_dict,Student_list = service_course_schedule.initialize_student(semester_str)
    time_used = public_function.get_time_used(start_time)
    print('初始化学生类列表完成,用时:', time_used)
    print('学生人数:',len(student_course_dict))

    # 设置学生选课
    print('设置学生选课列表开始')
    start_time = time.time()
    Student_list = service_course_schedule.set_student_enroll_course(Student_list,Course_list,student_course_dict)
    time_used = public_function.get_time_used(start_time)
    print('设置学生选课列表完成,用时:', time_used)
    
    # 种群大小和适应度阈值
    population_size_int = 100
    fitness_threshold_float = 50000
    # 保留最优的多少个
    retention_number_int=5

    print('排课种群初始化开始')
    start_time = time.time()
    # 获得初始化的种群
    PopulationList = initialize_population(Course_list, TimeSlot_list, Room_list, Student_list, population_size_int)
    time_used = public_function.get_time_used(start_time)
    print('排课种群初始化完成,用时:', time_used)

    # 初始化进化次数
    generation_int = 0
    while True:
        # 交叉和变异获得下一代种群
        print('排课种群进化开始')
        start_time = time.time()
        PopulationList = genetic_evolution(PopulationList,retention_number_int)
        time_used = public_function.get_time_used(start_time)
        print('排课种群进化完成,用时:', time_used)

        # 获取最优个体
        best_schedule = max(PopulationList, key=lambda x: x.fitness())
        best_fitness_float = best_schedule.fitness()

        # 打印当前代的最优适应度
        generation_int += 1
        print(f"Generation {generation_int}: Best Fitness = {best_fitness_float}")
        # best_schedule.display()
        print("-" * 40)

        # 如果达到了适应度要求，退出循环
        if best_fitness_float >= fitness_threshold_float:
            break

    print(f"best_fitness_float:{best_fitness_float},Final Best Schedule:")
    best_schedule.display()
