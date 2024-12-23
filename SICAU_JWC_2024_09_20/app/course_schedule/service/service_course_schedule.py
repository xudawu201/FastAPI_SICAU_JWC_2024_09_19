'''
Author: xudawu
Date: 2024-11-12 10:49:26
LastEditors: xudawu
LastEditTime: 2024-12-19 16:32:14
'''

# 遗传算法随机库
import random
import copy

# 引入模板模块
from app.course_schedule.model import model_course_schedule

# 遗传算法类
class GeneticAlgorithm:
    def __init__(self, Course_list, TimeSlot_list, Room_list, Student_list):
        self.Course_list = Course_list
        self.TimeSlot_list = TimeSlot_list
        self.Room_list = Room_list
        self.Student_list = Student_list
        # 初始化安排索引,键为四元组(周,天,讲,教室id)),值为Schedule类,用字典查找Schedule类优化性能
        self.ScheduleIndex_dict = {}
        # 根据校区和教室类型生成不同的课程字典,键是一个二元组 (校区, 教室类型),值为对应课程
        self.CourseByCampusAndType_dict = {}
        # 根据校区和教室类型生成不同的教室字典,键是一个二元组 (校区, 教室类型),值为对应教室
        self.RoomByCampusAndType_dict = {}
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
        self.schedule_experiment_course_type_name_str = '实验'
        
        # 初始化已删除没有匹配课程的教室列表
        self.NoMatchAreaOrTypeCourseRoom_list = []
        # 初始化已删除没有匹配课程已选人数的教室列表
        self.NoMatchCapacityCourseRoom_list = []

        # 初始化已删除没有匹配教室或容量的课程列表
        self.NoMatchAreaOrTypeAndCapacityRoomCourse_list = []

        # 教师上课次数字典,键为（周，天，教师id）,值为安排次数
        self.teacher_week_day_assigned_dict = {}
        # 初始化教师周安排次数字典,键位（周，教师id），值为安排次数
        self.teacher_week_assigned_dict = {}
        # 初始化安排理论课次数字典，键为（周，课程id）,值为安排次数
        self.theory_course_assigned_dict = {}
        # 初始化安排实验课次数字典，键为（周，课程id）,值为安排次数
        self.experiment_course_assigned_dict = {}
        # 初始化课程安排学时字典,键为（课程id）,值为已安排学时
        self.course_assigned_study_hour_dict = {}
        # 初始化课程id和课程类字典，键为课程id，值为课程类
        self.Course_id_dict = {}

        # 初始化理论课周和天安排次数,键为（周，天,课程id）,值为安排次数
        self.week_day_theory_course_assigned_dict = {}
        # 初始化实验课周和天安排次数,键为（周，天,课程id）,值为安排次数
        self.week_day_experiment_course_assigned_dict = {}
        # 连续天排课的理论课字典，键为（周，天,课程id）,值为课程id
        self.theory_course_continuous_count_dict = {}

        # 不正常课程安排标记，键为四元组(周,天,讲,教室id)),值为Schedule类,用字典查找Schedule类优化性能
        self.unnormal_schedule_dict = {}

        # 初始化排课安排列表和初始化安排索引
        for CurTimeSlot in self.TimeSlot_list:
            for CurRoom in self.Room_list:
                # 初始化排课安排列表
                schedule = model_course_schedule.Schedule(CurTimeSlot, CurRoom, None)

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

        # 初始化课程id和课程类字典
        for Course in self.Course_list:
            self.Course_id_dict[Course.id_int] = Course

        # 初始化字典结构以存储每个校区和教室类型的教室列表
        for CurRoom in self.Room_list:
            # 键是一个二元组 (校区, 教室类型)
            key = (CurRoom.campus_area_str, CurRoom.room_type_str)
            # 如果键不存在,则创建一个空列表
            if key not in self.RoomByCampusAndType_dict:
                self.RoomByCampusAndType_dict[key] = []
            # 将教室添加到列表中
            self.RoomByCampusAndType_dict[key].append(CurRoom)

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
            # print(f"没有找到符合类型条件的课程:{CurTimeSlot.week_time_int}{CurTimeSlot.day_time_int}{CurTimeSlot.slot_time_int}没有校区为{CurRoom.campus_area_str}，教室类型为{CurRoom.room_type_str}的课程")
            # 记录教室
            self.NoMatchAreaOrTypeCourseRoom_list.append(CurRoom)
            return None
        
        # 根据教室容量筛选符合条件的课程
        CapacityAvailableCourse_list = self.get_capacity_match_course_list(CurRoom,AvailableCourse_list)
        if CapacityAvailableCourse_list==[]:
            # print(f"没有找到符合容量条件的课程: 时间{CurTimeSlot.week_time_int}{CurTimeSlot.day_time_int}{CurTimeSlot.slot_time_int},{CurRoom.room_name_str} ({CurRoom.capacity_int}人) ")
            # 记录教室
            self.NoMatchCapacityCourseRoom_list.append(CurRoom)
            return None

        # 直接随机选择一门课程
        ChoiceCourse = random.choice(CapacityAvailableCourse_list)
        return ChoiceCourse

    # 批量处理2、4讲的实验课继承于1、3讲
    def batch_initialize_schedule_experiment_inherit(self,ScheduleIndex_dict):
        # 采用深拷贝,避免直接在原数据上修改
        CopyScheduleIndex_dict = copy.deepcopy(ScheduleIndex_dict)
        for Curkey,CurSchedule in CopyScheduleIndex_dict.items():
            if CurSchedule.Course!=None:
                # 处理实验课
                if CurSchedule.Course.schedule_course_type_str==self.schedule_experiment_course_type_name_str:
                    # 如果为可继承的起始讲(1、3)
                    if CurSchedule.TimeSlot.slot_time_int in self.experiment_inherit_start_slot_dict:
                        # 2、4讲继承
                        self.initialize_schedule_experiment_inherit(ScheduleIndex_dict.get(Curkey),ScheduleIndex_dict.get(Curkey).Course)

                    # 如果为2、4讲,且前一讲为理论课,设置次实验课失效排为None
                    if CurSchedule.TimeSlot.slot_time_int in self.experiment_inherit_slot_dict:
                        # 获得前一讲
                        pre_slot_key = (CurSchedule.TimeSlot.week_time_int, CurSchedule.TimeSlot.day_time_int, CurSchedule.TimeSlot.slot_time_int - 1,CurSchedule.Room.id_int)
                        PreSlotSchedule = self.ScheduleIndex_dict.get(pre_slot_key, None)
                        # 前一讲为空,则后一讲的实验课设置None
                        if PreSlotSchedule.Course==None :
                            # 安排课程为None
                            self.set_schedule_course(ScheduleIndex_dict.get(Curkey),None)
                        # 前一讲不为空，但为理论课页也设置为None
                        elif PreSlotSchedule.Course.schedule_course_type_str!=self.schedule_experiment_course_type_name_str:
                            # 安排课程为None
                            self.set_schedule_course(ScheduleIndex_dict.get(Curkey),None)

        return ScheduleIndex_dict

    # 删除无法排课的教室
    def delete_room_by_no_match_course(self):
    
        # 排课,遍历时间和教室的对应
        for (week_time_int, day_time_int,slot_time_int,room_id_int),CurSchedule in self.ScheduleIndex_dict.items():
            # 获得教室对应的课程
            ChoiceCourse = self.get_schedule(CurSchedule.TimeSlot,CurSchedule.Room)
        
        # 教室库删除没有类型和容量匹配的教室
        Room_list = [Room for Room in self.Room_list if Room not in self.NoMatchAreaOrTypeCourseRoom_list and Room not in self.NoMatchCapacityCourseRoom_list]

        CopyRoom_list = copy.deepcopy(Room_list)
        return CopyRoom_list

    # 根据课程找到合适的教室
    def get_room_by_course(self,Course):
        # 找到校区和教室对应
        key = (Course.campus_area_str, Course.room_type_str)
        ChoiceRoom_list = self.RoomByCampusAndType_dict.get(key,[])
        if ChoiceRoom_list==[]:
            # 没有找到合适的教室,则记录课程
            self.NoMatchAreaOrTypeAndCapacityRoomCourse_list.append(Course)
            return []
        # 获得容量匹配的教室列表
        CapacityAvailableRoom_list = [Room for Room in ChoiceRoom_list if Room.capacity_int>=Course.selected_student_num_int]
        if CapacityAvailableRoom_list==[]:
            # 没有找到合适的教室,则记录课程
            self.NoMatchAreaOrTypeAndCapacityRoomCourse_list.append(Course)
            return []
        
        return CapacityAvailableRoom_list

    # 根据课程随机设置课程的教室和时间
    def set_course_by_course(self,Course):
        
        # 根据课程找到合适的教室
        CapacityAvailableRoom_list = self.get_room_by_course(Course)
        # 没有找到合适的教室,直接返回
        if CapacityAvailableRoom_list==[]:
            return

        # 根据课程类别再对应排课
        schedule_course_type_str = Course.schedule_course_type_str
        # 获得当前课程需要排课的总学时
        cur_schedule_total_study_hour_int = int(Course.total_study_hour-Course.self_study_hour)

        # 初始化本次课所有可排课的安排
        CopyScheduleIndex_dict = {}
        # 获得所有教室id
        CapacityAvailableRoomId_list=[Room.id_int for Room in CapacityAvailableRoom_list]
        # 遍历所有安排,找到可以安排的安排
        for (week_time_int, day_time_int,slot_time_int,Room_id_int),CurSchedule in self.ScheduleIndex_dict.items():
            # 如果有课程,则不做更改
            if CurSchedule.Course!=None:
                continue
            # 如果是理论课,只选择工作日时间
            if schedule_course_type_str!=self.schedule_experiment_course_type_name_str:
                # 只选择工作日时间
                if day_time_int not in self.workday_day_time_dict:
                    continue
                # 排除周2第4讲
                if day_time_int==2 and slot_time_int==4:
                    continue
                # 排除周5第4、5讲
                if day_time_int==5 and slot_time_int in [4,5]:
                    continue
            else:
                # 实验课只选择1、3、5讲
                if slot_time_int not in self.experiment_start_slot_dict:
                    continue
                # 排除周2第4讲,对实验课来说,即为排除周2第3讲
                if day_time_int==2 and slot_time_int==3:
                    continue

            # 如果教室id不在可选择的教室id列表中,则跳过
            if Room_id_int not in CapacityAvailableRoomId_list:
                continue
            # 找到合适的安排,则安排课程
            CopyScheduleIndex_dict[(week_time_int, day_time_int,slot_time_int,Room_id_int)]=CurSchedule

        # 如果是理论课,选择时间需要排除周6,即只选择工作日时间
        if schedule_course_type_str!=self.schedule_experiment_course_type_name_str:
            # 一讲是两学时
            cur_schedule_total_study_hour_int = int(cur_schedule_total_study_hour_int/2)
            if cur_schedule_total_study_hour_int>len(CopyScheduleIndex_dict.keys()):
                # 课程学时大于可选择的时间,则无法安排此课程,记录课程
                self.NoMatchAreaOrTypeAndCapacityRoomCourse_list.append(Course)
                return
            # 根据课程学时选择对应的安排时间个数
            SampleScheduleIndex_list = random.sample(list(CopyScheduleIndex_dict.values()),k=cur_schedule_total_study_hour_int)
        else:
            # 如果是实验课,时间选择也减半
            cur_schedule_total_study_hour_int = int(cur_schedule_total_study_hour_int/4)
            if cur_schedule_total_study_hour_int>len(CopyScheduleIndex_dict.keys()):
                # 课程学时大于可选择的时间,则无法安排此课程,记录课程
                self.NoMatchAreaOrTypeAndCapacityRoomCourse_list.append(Course)
                return
            # 根据课程学时选择对应的安排时间个数
            SampleScheduleIndex_list = random.sample(list(CopyScheduleIndex_dict.values()),k=cur_schedule_total_study_hour_int)
        
        # 遍历时间安排课程
        for CurSampleSchedule in SampleScheduleIndex_list:
            # 找到随机位置
            Schedule_key = (CurSampleSchedule.TimeSlot.week_time_int, CurSampleSchedule.TimeSlot.day_time_int,CurSampleSchedule.TimeSlot.slot_time_int,CurSampleSchedule.Room.id_int)
            # 找到对应的安排
            ChoiceSchedule = self.ScheduleIndex_dict.get(Schedule_key,None)
            if ChoiceSchedule!=None:
                # 排实验课,只排1、3、5讲,2、4讲直接继承上一讲
                if schedule_course_type_str==self.schedule_experiment_course_type_name_str:
                    # 1、3、5讲直接排
                    if ChoiceSchedule.TimeSlot.slot_time_int in self.experiment_start_slot_dict:
                        self.initialize_schedule_experiment(ChoiceSchedule,Course)
                    # 如果是1、3讲,2、4讲继承
                    if ChoiceSchedule.TimeSlot.slot_time_int in self.experiment_inherit_start_slot_dict:
                        # 2、4讲继承
                        self.initialize_schedule_experiment_inherit(ChoiceSchedule,Course)
                # 排理论课
                else:
                    self.initialize_schedule_theory(ChoiceSchedule,Course)

    # 初始化基因,去掉不能排课的课程
    def initialize(self):
        
        # 排课,遍历课程
        for CurCourse in self.Course_list:
            # 随机设置课程
            self.set_course_by_course(CurCourse)
           
        # 课程库删除没有类型和容量匹配教室的课程
        Course_list = [Course for Course in self.Course_list if Course not in self.NoMatchAreaOrTypeAndCapacityRoomCourse_list]

        CopyCourse_list = copy.deepcopy(Course_list)
        return CopyCourse_list
    
    # 移动一门课
    def move_course(self,CurSchedule):
        # 随机找一个可以替换的位置

        # 根据原课程类别在对应排课
        schedule_course_type_str = CurSchedule.Course.schedule_course_type_str

        # 根据课程找到合适的教室
        CapacityAvailableRoom_list = self.get_room_by_course(CurSchedule.Course)
        # 没有找到合适的教室,直接返回
        if CapacityAvailableRoom_list==[]:
            return None
        
        # 随机选择一个教室
        ChoiceRoom = random.choice(list(CapacityAvailableRoom_list))
        if schedule_course_type_str!=self.schedule_experiment_course_type_name_str:
            # 随机一个时间,理论课需要在工作日时间,排除周2第4讲,排除周5第4、5讲
            CopyTimeSlot_list=[TimeSlot for TimeSlot in self.TimeSlot_list if TimeSlot.day_time_int in self.workday_day_time_dict and not (TimeSlot.day_time_int==2 and TimeSlot.slot_time_int==4) and not(TimeSlot.day_time_int==5 and TimeSlot.slot_time_int in [4,5])]
            # CopyTimeSlot_list=[TimeSlot for TimeSlot in self.TimeSlot_list if TimeSlot.day_time_int in self.workday_day_time_dict]
        else:
            # 实验课时间只在1、3、5讲,排除周2第3讲
            CopyTimeSlot_list=[TimeSlot for TimeSlot in self.TimeSlot_list if TimeSlot.slot_time_int in self.experiment_start_slot_dict and not (TimeSlot.day_time_int==2 and TimeSlot.slot_time_int==3)]
        ChoiceTimeSlot = random.choice(CopyTimeSlot_list)

        # 找到随机位置
        Schedule_key = (ChoiceTimeSlot.week_time_int, ChoiceTimeSlot.day_time_int,ChoiceTimeSlot.slot_time_int,ChoiceRoom.id_int)
        ChoiceSchedule = self.ScheduleIndex_dict.get(Schedule_key,None)
        # 不应原位置和新位置相同
        if ChoiceSchedule==CurSchedule:
            return True

        # 记录现位置的课程
        CurScheduleCourse = ChoiceSchedule.Course
        # 排实验课,只排1、3、5讲,2、4讲直接继承上一讲
        if schedule_course_type_str==self.schedule_experiment_course_type_name_str:
            # 1、3、5讲直接排
            if ChoiceSchedule.TimeSlot.slot_time_int in self.experiment_start_slot_dict:
                self.initialize_schedule_experiment(ChoiceSchedule,CurSchedule.Course)
            # 如果是1、3讲,2、4讲继承
            if ChoiceSchedule.TimeSlot.slot_time_int in self.experiment_inherit_start_slot_dict:
                # 2、4讲继承
                self.initialize_schedule_experiment_inherit(ChoiceSchedule,CurSchedule.Course)
        # 排理论课
        else:
            self.initialize_schedule_theory(ChoiceSchedule,CurSchedule.Course)

        # 返回原位置的课程
        return CurScheduleCourse

    # 设置课程
    def set_schedule_course_by_course(self,CurSchedule,ChoiceCourse):
        # 如果替换位置的课程为空,则用原位置的课程类别
        if ChoiceCourse==None:
            # 原位置有课,新位置无课,根据原位置的课程类别设置原位置安排为None
            schedule_course_type_str = CurSchedule.Course.schedule_course_type_str
            # 实验课还需要设置2、4讲
            if schedule_course_type_str==self.schedule_experiment_course_type_name_str:
                # 只在1、3、5讲排
                if CurSchedule.TimeSlot.slot_time_int in self.experiment_start_slot_dict:
                    self.initialize_schedule_experiment(CurSchedule,None)
                    # 如果是1、3讲,2、4讲继承
                if CurSchedule.TimeSlot.slot_time_int in self.experiment_inherit_start_slot_dict:
                    # 2、4讲继承
                    self.initialize_schedule_experiment_inherit(CurSchedule,None)
            # 如果是理论课,直接设置
            else:
                self.initialize_schedule_theory(CurSchedule,None)
        else:
            # 原位置有课,新位置也有课,根据新课程类别设置原位置安排
            schedule_course_type_str = ChoiceCourse.schedule_course_type_str
            # 实验课还需要设置2、4讲
            if schedule_course_type_str==self.schedule_experiment_course_type_name_str:
                # 只在1、3、5讲排
                if CurSchedule.TimeSlot.slot_time_int in self.experiment_start_slot_dict:
                    self.initialize_schedule_experiment(CurSchedule,ChoiceCourse)
                    # 如果是1、3讲,2、4讲继承
                if CurSchedule.TimeSlot.slot_time_int in self.experiment_inherit_start_slot_dict:
                    # 2、4讲继承
                    self.initialize_schedule_experiment_inherit(CurSchedule,ChoiceCourse)
            # 如果是理论课,直接设置
            else:
                self.initialize_schedule_theory(CurSchedule,ChoiceCourse)
                # 如果是原位置实验课,新位置理论课的情况，需要将原位置的实验课下一讲设置为None
                if CurSchedule.Course.schedule_course_type_str==self.schedule_experiment_course_type_name_str:
                    # 是最后一讲,直接返回
                    if CurSchedule.TimeSlot.slot_time_int+1>=6:
                        return
                    NextSchedule_key = (CurSchedule.TimeSlot.week_time_int, CurSchedule.TimeSlot.day_time_int,CurSchedule.TimeSlot.slot_time_int+1,CurSchedule.Room.id_int)
                    # 找到对应的安排
                    NextSchedule = self.ScheduleIndex_dict.get(NextSchedule_key,None)
                    # 更新课程安排
                    self.set_schedule_course(NextSchedule,None)

    # 基因变异操作
    def mutate(self):
        # 有一定概率不变异
        if random.random() < 0.2:
            # 直接中断返回
            return
        
        # 有一定概率选择安排不合适的安排
        if random.random() < 0.5:
            # 初始化安排不合理的安排
            self.get_unnormal_schedule_dict()
            # 安排字典继承
            CopyScheduleIndex_dict = self.unnormal_schedule_dict
        # 直接选择有课程安排的所有
        else:
            # 去掉课程安排为None的课程
            CopyScheduleIndex_dict = {key: value for key, value in self.ScheduleIndex_dict.items() if value.Course != None}

        # 交换两个课程
        if CopyScheduleIndex_dict=={}:
            return
        # 随机选择一个时间段和教室组合
        ChoiceSchedule = random.choice(list(CopyScheduleIndex_dict.values()))

        # 只交换有课程的
        if ChoiceSchedule.Course!=None:
            # 初始化安排继承
            ChoiceSchedule2 = ChoiceSchedule

            # 如果选择的是实验课,并且选择的是2、4讲,需要前移一讲
            if ChoiceSchedule.Course.schedule_course_type_str==self.schedule_experiment_course_type_name_str:
                # 如果当前为2、4讲,则前移1讲
                if ChoiceSchedule.TimeSlot.slot_time_int in self.experiment_inherit_slot_dict:
                    # 前移1讲
                    PreSchedule_key = (ChoiceSchedule.TimeSlot.week_time_int, ChoiceSchedule.TimeSlot.day_time_int,ChoiceSchedule.TimeSlot.slot_time_int-1,ChoiceSchedule.Room.id_int)
                    # 找到对应的安排
                    ChoiceSchedule2 = self.ScheduleIndex_dict.get(PreSchedule_key,None)

            # 移动课程
            CurScheduleCourse = self.move_course(ChoiceSchedule2)
            # 新旧位置相同,则直接返回
            if CurScheduleCourse==True:
                return
            # 设置原位置课程为移动位置的课程
            self.set_schedule_course_by_course(ChoiceSchedule2,CurScheduleCourse)

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
                    fitness_float -= 2
                    # 记录冲突信息
                    self.conflict_info_list.append((CurStudent.student_id_str, CurCourse.id_int, CurTimeSlot))

                # 更新学生的时间段表,增加此上课时间到学生的上课时间表中
                else:
                    CurStudent.TimeSlotList.append(CurTimeSlot)

        return fitness_float

    # 计算课程安排学时适应度
    def course_schedule_study_hour_fitness(self,course_assigned_study_hour_dict):
        # 初始化学时适应度
        study_hour_fitness_float = 0
        for cur_key,cur_study_hour in course_assigned_study_hour_dict.items():
            CurCourse = self.Course_id_dict.get(cur_key,None)
            if CurCourse!=None:
                # 获得当前课程需要排课的总学时
                cur_schedule_total_study_hour_float = CurCourse.total_study_hour-CurCourse.self_study_hour
                # 总学时减去已排学时的绝对值,即为和要求排课的距离,为0则为最佳
                study_hour_distance_float= abs(cur_schedule_total_study_hour_float-cur_study_hour*2)
                # 距离为0增加大量适应度
                if study_hour_distance_float==0:
                    study_hour_fitness_float += 1
                # 距离越大,适应度越低,直接减去距离和一个基础值
                else:
                    study_hour_fitness_float -= study_hour_distance_float
                    # study_hour_fitness_float -= 1
        return study_hour_fitness_float

    # 计算课程隔天排课适应度
    def course_schedule_day_fitness(self,course_assigned_dict):
        # 初始化连续排课的字典
        self.theory_course_continuous_count_dict = {}
        # 初始化适应度
        fitness_float = 0
        # 初始化课程id
        for (week_time_int,day_time_int,course_id_int), course_assigned_count_int in course_assigned_dict.items():
            # 跳过安排次数为0的课
            if course_assigned_count_int==0:
                continue
            # 跳过周六及以后的时间
            if day_time_int>=6:
                continue
            next_key = (week_time_int,day_time_int+1,course_id_int)
            next_course_assigned_count_int = course_assigned_dict.get(next_key,0)
            # 适应度减去下一天的课程安排次数
            fitness_float -= next_course_assigned_count_int

            # 如果下一天有课程安排,更新连续排课的字典
            if next_course_assigned_count_int!=0:
                # 更新连续排课的字典
                self.theory_course_continuous_count_dict[(week_time_int,day_time_int,course_id_int)] = course_id_int
                self.theory_course_continuous_count_dict[(next_key)] = course_id_int

        return fitness_float
    
    # 计算教师安排次数适应度
    def teacher_schedule_week_day_fitness(self,teacher_week_day_assigned_dict):
        # 初始化适应度
        fitness_float = 0
        # 初始化天数适应度
        day_fitness_float = 0
        # 初始化周次数适应度
        week_fitness_float = 0
        # 初始化教师周安排次数字典
        self.teacher_week_assigned_dict = {}
        
        # 初始化已处理教师列表
        teacher_processed_id_list = []
        for (week_time_int,day_time_int,teacher_id_int),schedule_count_int in teacher_week_day_assigned_dict.items():
            # 计算教师本周安排次数
            teacher_week_key = (week_time_int,teacher_id_int)
            # 跳过已处理过的教师
            if teacher_week_key in teacher_processed_id_list:
                continue
            # 更新已处理教师列表
            teacher_processed_id_list.append(teacher_week_key)
            # 初始化安排次数为0
            self.teacher_week_assigned_dict[teacher_week_key] = 0

            # 遍历安排字典
            for (cur_week_time_int,cur_ay_time_int,cur_teacher_id_int),schedule_count_int in teacher_week_day_assigned_dict.items():
                if teacher_week_key == (cur_week_time_int,cur_teacher_id_int):
                    # 更新教师周安排次数
                    self.teacher_week_assigned_dict[teacher_week_key] += schedule_count_int

            # 计算周安排课次数适应度,大于12次为不合理
            if self.teacher_week_assigned_dict[teacher_week_key]>12:
                week_fitness_float -= self.teacher_week_assigned_dict[teacher_week_key]-12
            # 12次内为合理
            else:
                week_fitness_float += 1

            # 计算一天安排课次数适应度,0、1、2次合理
            if schedule_count_int<=2:
                day_fitness_float += 2
            # 3次为稍微不合理
            elif schedule_count_int==3:
                day_fitness_float += 1
            # 3次以上不合理,直接减去安排次数
            else:
                day_fitness_float -= schedule_count_int-3

        # 计算教师周安排适应度
        fitness_float += day_fitness_float
        fitness_float += week_fitness_float
        return fitness_float

    # 计算教师连堂上课的适应度
    def teacher_schedule_continuous_fitness(self):
        # 初始化适应度
        fitness_float = 0
        # 初始化连续上课次数
        continuous_count_int = 0
        # 初始化连续上课次数字典
        self.teacher_course_continuous_count_dict = {}
        # 初始化已处理教师列表
        teacher_processed_id_list = []

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
                teacher_week_day_time_list=[]
                for CurTimeSlot in self.TimeSlot_list:
                    teacher_key = (CurTimeSlot.week_time_int,CurTimeSlot.day_time_int,CurTeacher.id_int)
                    # 如果是没处理过的教师
                    if teacher_key not in teacher_week_day_time_list:
                        # 更新已处理周和天数
                        teacher_week_day_time_list.append(teacher_key)
                        self.teacher_week_day_assigned_dict[teacher_key] = 0

            # 初始化已处理周数
            course_week_time_list=[]
            # 初始化已处理周和天数
            course_week_day_time_list=[]
            for CurTimeSlot in self.TimeSlot_list:
                if CurTimeSlot.week_time_int not in course_week_time_list:
                    # 更新已处理周数
                    course_week_time_list.append(CurTimeSlot.week_time_int)
                    key = (CurTimeSlot.week_time_int,CurCourse.id_int)
                    # 排课类别为实验的课程,初始化课程被安排的次数
                    if CurCourse.schedule_course_type_str == self.schedule_experiment_course_type_name_str:
                        self.experiment_course_assigned_dict[key] = 0
                    # 理论课的课程,初始化课程被安排的次数
                    else:
                        self.theory_course_assigned_dict[key] = 0

                # 更新课程按周和天的排课次数
                cur_week_day_key = (CurTimeSlot.week_time_int,CurTimeSlot.day_time_int,CurCourse.id_int)
                if cur_week_day_key not in course_week_day_time_list:
                    # 更新课程按周和天的排课次数
                    course_week_day_time_list.append(cur_week_day_key)
                    # 排课类别为实验的课程,初始化课程被安排的次数
                    if CurCourse.schedule_course_type_str == self.schedule_experiment_course_type_name_str:
                        self.week_day_experiment_course_assigned_dict[cur_week_day_key] = 0
                    # 理论课的课程,初始化课程被安排的次数
                    else:
                        self.week_day_theory_course_assigned_dict[cur_week_day_key] = 0

            # 初始化课程已安排学时为0
            key = (CurCourse.id_int)
            self.course_assigned_study_hour_dict[key] = 0
                        
        # 计算适应度
        for CurSchedule in self.ScheduleIndex_dict.values():
            # 如果当前时段有课程安排,则进行判断
            if CurSchedule.Course is not None:
                # 同一课程同一时间不能安排在多个教室,同一时间同一课程名代表有冲突
                # 在安排中则代表有冲突
                if (CurSchedule.TimeSlot, CurSchedule.Room) in course_time_dict:
                    fitness_float -= 2
                else:
                    # 没有在安排表中，记录此次安排
                    course_time_dict[(CurSchedule.TimeSlot, CurSchedule.Room)] = CurSchedule.Course
                    
                # 安排此课,适应度分值加上优先级分值
                # fitness_float += CurSchedule.Course.priority_float
                # 统计教师被安排的次数
                for CurTeacher in CurSchedule.Course.CourseTeacher_list:
                    teacher_key=(CurSchedule.TimeSlot.week_time_int,CurSchedule.TimeSlot.day_time_int,CurTeacher.id_int)
                    # 如果是实验课并且安排在第5讲,算排了两次课
                    if CurSchedule.Course.schedule_course_type_str == self.schedule_experiment_course_type_name_str and CurSchedule.TimeSlot.slot_time_int in self.experiment_course_count_double_slot_dict:
                        self.teacher_week_day_assigned_dict[teacher_key] += 2
                    else:
                        self.teacher_week_day_assigned_dict[teacher_key] += 1
                        
                # 分别计算理论课和实验课被安排的次数
                key = (CurSchedule.TimeSlot.week_time_int,CurSchedule.Course.id_int)
                # 计算课程学时
                course_key=(CurSchedule.Course.id_int)
                # 获得（周、天、课程id）的key
                cur_week_day_key = (CurSchedule.TimeSlot.week_time_int,CurSchedule.TimeSlot.day_time_int,CurSchedule.Course.id_int)
                if CurSchedule.Course.schedule_course_type_str == self.schedule_experiment_course_type_name_str:
                    # 如果是第5讲,算排了两次课
                    if CurSchedule.TimeSlot.slot_time_int in self.experiment_course_count_double_slot_dict:
                        self.experiment_course_assigned_dict[key] +=2
                        # 课时加4
                        self.course_assigned_study_hour_dict[course_key]+=4

                        # 实验课按周和天的排课次数加1
                        self.week_day_experiment_course_assigned_dict[cur_week_day_key] += 2
                    else:
                        self.experiment_course_assigned_dict[key] +=1
                        # 课时加2
                        self.course_assigned_study_hour_dict[course_key]+=2

                        # 实验课按周和天的排课次数加1
                        self.week_day_experiment_course_assigned_dict[cur_week_day_key] += 1
                # 是理论课
                else:
                    self.theory_course_assigned_dict[key] += 1
                    # 课时加2
                    self.course_assigned_study_hour_dict[course_key]+=2

                    # 理论课按周和天的排课次数加1
                    self.week_day_theory_course_assigned_dict[cur_week_day_key] += 1


                # 计算该课程学生相关适应度
                student_fitness_float = self.student_fitness(CurSchedule.TimeSlot,CurSchedule.Course)
                fitness_float += student_fitness_float

                # 如果此门课程的安排时间在教师不可以上课的时间列表中，适应度大幅降低
                for CourseTeacher in CurSchedule.Course.CourseTeacher_list:
                    for TeacherUnavailableTimeSlot in CourseTeacher.unavailable_timeslot_list:
                        if CurSchedule.TimeSlot.day_time_int == TeacherUnavailableTimeSlot.day_time_int and CurSchedule.TimeSlot.slot_time_int == TeacherUnavailableTimeSlot.slot_time_int :
                            fitness_float -= 2

        # 理论课周排课均衡性评分
        for (week_time_int,course_id_int), course_assigned_count_int in self.theory_course_assigned_dict.items():
            # 小于1次
            if course_assigned_count_int <1:
                fitness_float -= 2
            # 1-2次排课,即2-4周学时是合理的
            elif 1<= course_assigned_count_int <= 2:
                fitness_float += 2
            # 3次排课,即6周学时是稍微不合理的
            elif course_assigned_count_int == 3:
                fitness_float += 1
            # 其他情况,直接减去排课次数的分,次数越多减的越多,增加减去一个基础分,消除边界波动
            else:
                fitness_float -= course_assigned_count_int-3

        # 实验课周排课均衡性评分
        for (week_time_int,course_id_int), course_assigned_count_int in self.experiment_course_assigned_dict.items():
            # print((week_time_int,course_id_int), course_assigned_count_int)
            # 小于2次
            if course_assigned_count_int <1:
                fitness_float -= 2
            # 1-4次排课,即2-8周学时是合理的
            elif 1<= course_assigned_count_int <= 4:
                fitness_float += 1
            # 其他情况,直接减去排课次数的分,次数越多减的越多,增加减去一个基础分
            else:
                fitness_float -= course_assigned_count_int-4

        # 课程学时安排适应度
        # fitness_float += self.course_schedule_study_hour_fitness(self.course_assigned_study_hour_dict)
        # 课程隔天排课适应度
        fitness_float += self.course_schedule_day_fitness(self.week_day_theory_course_assigned_dict)

        # 教师周和天上课次数适应度
        fitness_float += self.teacher_schedule_week_day_fitness(self.teacher_week_day_assigned_dict)

        # 返回适应度
        return fitness_float

    # 找到课程本周的安排的讲数
    def get_course_assigned_count(self,CurTimeSlot,CurCourse):
        # 获得key键
        key=(CurTimeSlot.week_time_int,CurCourse.id_int)
        # 处理实验课
        if CurCourse.schedule_course_type_str == self.schedule_experiment_course_type_name_str:
            schedule_week_count_int = self.experiment_course_assigned_dict.get(key,-1)
            return schedule_week_count_int
        # 处理理论课
        else:
            schedule_week_count_int = self.theory_course_assigned_dict.get(key,-1)
            return schedule_week_count_int
    
    # 更新课程按周和天安排的字典
    def update_week_day_course_assigned_dict(self):
        # 每个教师和课程被安排的次数初始化为0
        for CurCourse in self.Course_list:
            # 初始化已处理周和天数
            course_week_day_time_list=[]
            for CurTimeSlot in self.TimeSlot_list:

                # 更新课程按周和天的排课次数
                cur_week_day_key = (CurTimeSlot.week_time_int,CurTimeSlot.day_time_int,CurCourse.id_int)
                if cur_week_day_key not in course_week_day_time_list:
                    # 更新课程按周和天的排课次数
                    course_week_day_time_list.append(cur_week_day_key)
                    # 排课类别为实验的课程,初始化课程被安排的次数
                    if CurCourse.schedule_course_type_str == self.schedule_experiment_course_type_name_str:
                        self.week_day_experiment_course_assigned_dict[cur_week_day_key] = 0
                    # 理论课的课程,初始化课程被安排的次数
                    else:
                        self.week_day_theory_course_assigned_dict[cur_week_day_key] = 0
                        
        # 设置已安排课程时间
        for CurSchedule in self.ScheduleIndex_dict.values():
            # 如果当前时段有课程安排,则进行判断
            if CurSchedule.Course is not None:
                # 获得（周、天、课程id）的key
                cur_week_day_key = (CurSchedule.TimeSlot.week_time_int,CurSchedule.TimeSlot.day_time_int,CurSchedule.Course.id_int)
                if CurSchedule.Course.schedule_course_type_str == self.schedule_experiment_course_type_name_str:
                    # 如果是第5讲,算排了两次课
                    if CurSchedule.TimeSlot.slot_time_int in self.experiment_course_count_double_slot_dict:

                        # 实验课按周和天的排课次数加1
                        self.week_day_experiment_course_assigned_dict[cur_week_day_key] += 2
                    else:

                        # 实验课按周和天的排课次数加1
                        self.week_day_experiment_course_assigned_dict[cur_week_day_key] += 1
                # 是理论课
                else:

                    # 理论课按周和天的排课次数加1
                    self.week_day_theory_course_assigned_dict[cur_week_day_key] += 1

    # 获得不正常安排的标记字典
    def get_unnormal_schedule_dict(self):
        
        # 更新按周和天的排课次数字典
        self.update_week_day_course_assigned_dict()

        # 初始化不正常安排字典
        self.unnormal_schedule_dict = {}

        # 遍历所有排课
        for CurSchedule in self.ScheduleIndex_dict.values():
            # 如果课程为非空,则打印课程信息
            if CurSchedule.Course !=None:

                # 检查教师是否在不可上课时间
                for CurTeacher in CurSchedule.Course.CourseTeacher_list:
                    if CurSchedule.TimeSlot in CurTeacher.unavailable_timeslot_list:
                        # 标记此安排
                        schedule_key = (CurSchedule.TimeSlot.week_time_int, CurSchedule.TimeSlot.day_time_int, CurSchedule.TimeSlot.slot_time_int,CurSchedule.Room.id_int)
                        self.unnormal_schedule_dict[schedule_key] = CurSchedule


                # 初始化学生上课时间冲突信息
                for (student_id_str, cur_course_id_int, CurTimeSlot) in self.conflict_info_list:
                    if cur_course_id_int == CurSchedule.Course.id_int and CurTimeSlot == CurSchedule.TimeSlot:

                        # 标记此安排
                        schedule_key = (CurSchedule.TimeSlot.week_time_int, CurSchedule.TimeSlot.day_time_int, CurSchedule.TimeSlot.slot_time_int,CurSchedule.Room.id_int)
                        self.unnormal_schedule_dict[schedule_key] = CurSchedule
                
                # 找到本周此课程安排次数(讲数)
                schedule_week_count_int = self.get_course_assigned_count(CurSchedule.TimeSlot,CurSchedule.Course)
                # 属于实验课
                if CurSchedule.Course.schedule_course_type_str == self.schedule_experiment_course_type_name_str:
                    # 如果讲数不在2-4之间
                    if schedule_week_count_int<1 or 4<schedule_week_count_int:
                        # 标记此安排
                        schedule_key = (CurSchedule.TimeSlot.week_time_int, CurSchedule.TimeSlot.day_time_int, CurSchedule.TimeSlot.slot_time_int,CurSchedule.Room.id_int)
                        self.unnormal_schedule_dict[schedule_key] = CurSchedule
                # 理论课在1-2次之间
                else:
                    # 如果讲数不在2-4之间
                    if schedule_week_count_int<1 or 2<schedule_week_count_int:
                        # 标记此安排
                        schedule_key = (CurSchedule.TimeSlot.week_time_int, CurSchedule.TimeSlot.day_time_int, CurSchedule.TimeSlot.slot_time_int,CurSchedule.Room.id_int)
                        self.unnormal_schedule_dict[schedule_key] = CurSchedule
                
                # 更新此课程是否隔天排课
                cur_continuous_course_key = (CurSchedule.TimeSlot.week_time_int,CurSchedule.TimeSlot.day_time_int,CurSchedule.Course.id_int)
                cur_continuous_course_id_int = self.theory_course_continuous_count_dict.get(cur_continuous_course_key,None)
                # 如果存在,说明此课程没有间隔一天排课
                if cur_continuous_course_id_int != None:
                    # 标记此安排
                    schedule_key = (CurSchedule.TimeSlot.week_time_int, CurSchedule.TimeSlot.day_time_int, CurSchedule.TimeSlot.slot_time_int,CurSchedule.Room.id_int)
                    self.unnormal_schedule_dict[schedule_key] = CurSchedule

        for CurSchedule in self.unnormal_schedule_dict.values():
            if CurSchedule.Course == None:
                print('aaaaa',CurSchedule.TimeSlot.week_time_int, CurSchedule.TimeSlot.day_time_int, CurSchedule.TimeSlot.slot_time_int,CurSchedule.Room.id_int)
        
    def display(self):

        # 未安排课程字典
        unassigned_course_dict = {}
        # 初始化当前代排课信息字典
        current_generation_info_dict = {
            # 初始化当前代排课信息
            "room_assigned_course_schedule_dict": {},
        }
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
        # 初始化未安排时间列表
        unassigned_time_list = set(self.TimeSlot_list)

        # 初始化排课索引
        schedule_index_int = 0
        # 初始化上课时间冲突教师列表
        schedule_conflict_time_teachers_list = []
        # 初始化上课时间冲突学生列表
        schedule_conflict_time_student_list = []
        for CurSchedule in self.ScheduleIndex_dict.values():
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
                enrolled_course_student_str = ",".join(enrolled_course_student_name_list) if enrolled_course_student_name_list else "No student enrolled"

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
                for (student_id_str, cur_course_id_int, CurTimeSlot) in self.conflict_info_list:
                    if cur_course_id_int == CurSchedule.Course.id_int and CurTimeSlot == CurSchedule.TimeSlot:
                        conflict_str = f"{student_id_str}"

                        # 添加学生上课时间冲突表
                        schedule_conflict_time_student_list.append(cur_course_id_int)
                
                # 找到教师
                teacher_id_str = ''
                for CurTeacher in CurSchedule.Course.CourseTeacher_list:
                    teacher_id_str+=str(CurTeacher.id_int)+','
                # 排课时间、教师、课程名、授课教师、课程优先级、选课学生、冲突信息、是否处于教师不可上课时间、不可上课信息
                # room_course_schedule_str = f"week:{CurSchedule.TimeSlot.week_time_int},day:{CurSchedule.TimeSlot.day_time_int},time:{CurSchedule.TimeSlot.slot_time_int} in {CurSchedule.Room.room_name_str}: {CurSchedule.Course.name_str} by {teacher_id_str} (Priority: {CurSchedule.Course.priority_float}) | Enrolled: {enrolled_course_student_str} | student_conflict:{conflict_str} | teacher_availability:{availability_str}"
                
                # 初始化课程教师一天上课次数
                course_teacher_day_schedule_count_list=[]
                # 初始化课程教师一周上课次数
                course_teacher_week_schedule_count_list = []

                # 初始化处理教师不可上课时间为列表
                teatcher_unavailable_timeslot_list=[]
                for CurTeacher in CurSchedule.Course.CourseTeacher_list:
                    # 如果有不可上课时间
                    if CurTeacher.unavailable_timeslot_list != []:
                        for ThisCurTimeSlot in CurTeacher.unavailable_timeslot_list:
                            this_cur_time_slot_list=[f'week:{ThisCurTimeSlot.week_time_int},day:{ThisCurTimeSlot.day_time_int},time:{ThisCurTimeSlot.slot_time_int}']
                            teatcher_unavailable_timeslot_list.append(this_cur_time_slot_list)

                    # 设置课程教师一天上课次数
                    week_day_key =(CurSchedule.TimeSlot.week_time_int,CurSchedule.TimeSlot.day_time_int,CurTeacher.id_int)
                    course_teacher_day_schedule_count_list.append(self.teacher_week_day_assigned_dict.get(week_day_key,0))

                    # 设置课程教师一天上课次数
                    week_key =(CurSchedule.TimeSlot.week_time_int,CurTeacher.id_int)
                    course_teacher_week_schedule_count_list.append(self.teacher_week_assigned_dict.get(week_key,0))

                if course_teacher_day_schedule_count_list==[]:
                    course_teacher_day_schedule_count_str='无'
                else:
                    # 教师上课次数转为字符串
                    course_teacher_day_schedule_count_str = ','.join(str(count_int) for count_int in course_teacher_day_schedule_count_list)

                if course_teacher_week_schedule_count_list==[]:
                    course_teacher_week_schedule_count_str='无'
                else:
                    course_teacher_week_schedule_count_str = ','.join(str(count_int) for count_int in course_teacher_week_schedule_count_list)

                # 转化为字符串
                teatcher_unavailable_timeslot_str=''
                for cur_time_slot in teatcher_unavailable_timeslot_list:
                    teatcher_unavailable_timeslot_str+=cur_time_slot+','
                # 找到本周此课程安排次数(讲数)
                schedule_week_count_int = self.get_course_assigned_count(CurSchedule.TimeSlot,CurSchedule.Course)
                # 找到本课程已排学时和要求排课的距离
                CurCourse = self.Course_id_dict.get((CurSchedule.Course.id_int),None)
                # 初始化学时要求
                cur_schedule_total_study_hour_float=0
                # 初始化已排总学时
                cur_study_hour=0
                if CurCourse!=None:
                    # 获得当前课程需要排课的总学时
                    cur_schedule_total_study_hour_float = CurCourse.total_study_hour-CurCourse.self_study_hour
                    key = (CurCourse.id_int)
                    cur_study_hour = self.course_assigned_study_hour_dict.get(key,0)
                    # 总学时减去已排学时的绝对值,即为和要求排课的距离,为0则为最佳
                    study_hour_distance_float= abs(cur_schedule_total_study_hour_float-cur_study_hour)

                # 更新此课程是否隔天排课
                is_contitueous_course_bool = 'false'
                cur_continuous_course_key = (CurSchedule.TimeSlot.week_time_int,CurSchedule.TimeSlot.day_time_int,CurSchedule.Course.id_int)
                cur_continuous_course_id_int = self.theory_course_continuous_count_dict.get(cur_continuous_course_key,None)
                # 如果存在,说明此课程没有间隔一天排课
                if cur_continuous_course_id_int != None:
                    is_contitueous_course_bool = 'true'

                # 添加到字典中,使用排课安排索引作为键,值为排课信息
                current_generation_info_dict["room_assigned_course_schedule_dict"][f'schedule{schedule_index_int}']={
                    'week':CurSchedule.TimeSlot.week_time_int,'day':CurSchedule.TimeSlot.day_time_int,
                    "time":CurSchedule.TimeSlot.slot_time_int,"room":CurSchedule.Room.room_name_str,
                    "course":CurSchedule.Course.name_str,"teacher":teacher_id_str,"priority":CurSchedule.Course.priority_float,
                    "enrolled_student":enrolled_course_student_str,"conflict":conflict_str,"availability":availability_str,
                    'unavailable_timeslots_teacher':teatcher_unavailable_timeslot_str, 
                    
                    'schedule_course_type':CurSchedule.Course.schedule_course_type_str,
                    'campus_area_str':CurSchedule.Room.campus_area_str,
                    'schedule_week_count_int':schedule_week_count_int,
                    'study_hour_distance_float':study_hour_distance_float,
                    'cur_schedule_total_study_hour_float':cur_schedule_total_study_hour_float,
                    'cur_study_hour':cur_study_hour,
                    'course_id':CurSchedule.Course.id_int,
                    'room_id':CurSchedule.Room.id_int,
                    'is_contitueous_course_bool':is_contitueous_course_bool,
                    
                    'course_teacher_day_study_hour_str':course_teacher_day_schedule_count_str,
                    'course_teacher_week_study_hour_str':course_teacher_week_schedule_count_str,
                    }

                # 从未安排列表中移除教室
                unassigned_rooms.discard(CurSchedule.Room)
                try:
                    # 将已排的课从未安排课中移除
                    removed_value = unassigned_course_dict.pop(CurSchedule.Course.id_int)
                except KeyError:
                    # 键不存在,则跳过
                    pass
                # 更新未安排时间列表
                unassigned_time_list.discard(CurSchedule.TimeSlot)

            else:
                # room_course_schedule_str = f"week:{CurSchedule.TimeSlot.week_time_int},day:{CurSchedule.TimeSlot.day_time_int},time:{CurSchedule.TimeSlot.slot_time_int} in {CurSchedule.Room.room_name_str}: Free"
                current_generation_info_dict["room_assigned_course_schedule_dict"][f'schedule{schedule_index_int}']={
                    'week':CurSchedule.TimeSlot.week_time_int,'day':CurSchedule.TimeSlot.day_time_int,
                    "time":CurSchedule.TimeSlot.slot_time_int,"room":CurSchedule.Room.room_name_str,
                    "course":'未安排排课',"teacher":'',"priority":'',"enrolled_student":'',"conflict":'',
                    "availability":'','unavailable_timeslots_teacher':'',

                    'schedule_course_type':'',
                    'campus_area_str':CurSchedule.Room.campus_area_str,
                    'schedule_week_count_int':'',
                    'study_hour_distance_float':'',
                    'cur_schedule_total_study_hour_float':'',
                    'cur_study_hour':'',
                    'course_id':'',
                    'room_id':CurSchedule.Room.id_int,
                    'is_contitueous_course_bool':'false',

                    'course_teacher_day_study_hour_str':'',
                    'course_teacher_week_study_hour_str':'',
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
        if unassigned_time_list:
            unique_unassigned_time_list_str=''
            for CurTimeSlot in unassigned_time_list:
                unique_unassigned_time_list_str+=f'({CurTimeSlot.week_time_int},{CurTimeSlot.day_time_int},{CurTimeSlot.slot_time_int})'
                unique_unassigned_time_list_str+='_'
        else:
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
            unassigned_student_str = "" + ",".join(unassigned_students)
        else:
            unassigned_student_str = "无"
        # 添加到字典中
        current_generation_info_dict["unassigned_student_list"]=unassigned_student_str
        # print('unassigned_student_str:',unassigned_student_str)

        # 初始化不正常安排
        unnormal_schedule_str = ''
        # 初始化安排不合理的安排字典,确保及时更新数据
        self.get_unnormal_schedule_dict()
        
        for CurSchedule in self.unnormal_schedule_dict.values():
            unnormal_schedule_str+=f'({CurSchedule.Course.id_int}_{CurSchedule.Course.name_str}),'

        if unnormal_schedule_str == '':
            unnormal_schedule_str = "无"
        # 添加到字典中
        current_generation_info_dict["unnormal_schedule_str"]=unnormal_schedule_str

        # 教师上课次数字典,键为（周，天，教师id）,值为安排次数
        self.teacher_week_day_assigned_dict = {}
        # 初始化教师周安排次数字典,键位（周，教师id），值为安排次数
        self.teacher_week_assigned_dict = {}

        # 初始化教师一天上课次数不合理
        unnormal_schedule_teacher_day_str = ''
        for (week_int,day_int,teacher_id_int),teacher_day_schedule_count_int in self.teacher_week_day_assigned_dict.values():
            # 标记大于等于3次的
            if teacher_day_schedule_count_int>=3:
                unnormal_schedule_teacher_day_str+=f'({week_int}_{day_int}_{teacher_id_int}_{teacher_day_schedule_count_int}),'

        if unnormal_schedule_teacher_day_str == '':
            unnormal_schedule_teacher_day_str = "无"
        # 添加到字典中
        current_generation_info_dict["unnormal_schedule_teacher_day_str"]=unnormal_schedule_teacher_day_str

        # 初始化教师一周上课次数不合理
        unnormal_schedule_teacher_week_str = ''
        for (week_int,teacher_id_int),teacher_week_schedule_count_int in self.teacher_week_assigned_dict.values():
            # 标记大于12次的
            if teacher_week_schedule_count_int>12:
                unnormal_schedule_teacher_week_str+=f'({week_int}_{teacher_id_int}_{teacher_week_schedule_count_int}),'

        if unnormal_schedule_teacher_week_str == '':
            unnormal_schedule_teacher_week_str = "无"
        # 添加到字典中
        current_generation_info_dict["unnormal_schedule_teacher_week_str"]=unnormal_schedule_teacher_week_str

        return current_generation_info_dict

# 列表去重并拼接
def list_remove_duplicate_joint(cur_list):
    # 用集合去重
    # cur_set=set(cur_list)
    # 再转为列表
    unique_list=list(cur_list)

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

    # 删除不能排课的教室
    CopyRoom_list = SingleSchedule.delete_room_by_no_match_course()
    # 如果课程列表空,则中断排课
    if CopyRoom_list == []:
        return True

    # 实例化一个个体,使用修改后的教室列表
    SingleSchedule = GeneticAlgorithm(Course_list, TimeSlot_list, CopyRoom_list, Student_list)
    # 对个体的基因进行随机初始化
    # 随机一个基因(对时间段和教室的组合随机选择一门课)
    CopyCourse_list = SingleSchedule.initialize()

    # 如果课程列表空,则中断排课
    if CopyCourse_list == []:
        couse_list_is_empty=True
        return couse_list_is_empty

    # 种群列表初始化
    Population_list = []
    # count_int=0
    for count_int in range(population_size):
        # print(f'count:{count_int+1}/{population_size},初始化单个个体开始')
        # start_time = time.time()
        # 实例化一个个体
        SingleSchedule = GeneticAlgorithm(CopyCourse_list, TimeSlot_list, CopyRoom_list, Student_list)
        # 对个体的基因进行随机初始化
        # 随机一个基因(对时间段和教室的组合随机选择一门课)
        CopyCourse2_list = SingleSchedule.initialize()

        # 将初始化后的个体加入种群列表
        Population_list.append(SingleSchedule)
        # time_used = public_function.get_time_used(start_time)
        # print('初始化单个个体完成,用时:', time_used)
    # 返回初始化的种群列表
    return Population_list
