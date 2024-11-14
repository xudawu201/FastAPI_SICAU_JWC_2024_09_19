'''
Author: xudawu
Date: 2024-09-18 16:39:56
LastEditors: xudawu
LastEditTime: 2024-11-14 18:01:32
'''
# 遗传算法随机库
import random

# fastapi相关
from fastapi import APIRouter, Request,WebSocket
# 引入模板模块
from template import TemplatesJinja2CourseSchedule
# 引入数据库模块
from database import database_connection
import asyncio


# 全局超参数

router = APIRouter()

# 设置是否停止排课的标志
is_stop_schedule = False



class Course:
    def __init__(self, name_str, teacher_str, duration_float, priority_float=1, unavailable_timeslots_list=[]):
        self.name_str = name_str
        self.teacher_str = teacher_str
        self.duration_float = duration_float
        self.priority_float = priority_float
        # 不可用的时间列表
        self.unavailable_timeslots_list = unavailable_timeslots_list if unavailable_timeslots_list else []

class Student:
    def __init__(self, name_str):
        self.name_str = name_str
        self.enrolled_courses_list = []
        # 记录学生的上课时间段
        self.time_slots_list = []

    def enroll(self, course):
        self.enrolled_courses_list.append(course)

class Schedule:
    def __init__(self, course_list, timeslots_list, room_list, student_list):
        self.course_list = course_list
        self.timeslots_list = timeslots_list
        self.room_list = room_list
        self.student_list = student_list
        # 时段和教室的组合作为键，课程作为值,课程初始化为None
        self.schedule_dict = {}
        for cur_timeslot_str in self.timeslots_list:
            for cur_room_str in self.room_list:
                self.schedule_dict[(cur_timeslot_str, cur_room_str)] = None

    def fitness(self):
        fitness_float = 0
        course_time_dict = {}
        teacher_assigned_dict = {}

        # 初始化学生冲突时间表为空列表
        for CurStudent in self.student_list:
            CurStudent.time_slots_list = []

        # 初始化冲突信息的列表
        self.conflict_info_list = []

        # 每个教师被安排的次数初始化为0
        for CurCourse in self.course_list:
            teacher_assigned_dict[CurCourse.teacher_str] = 0
        
        for (cur_timeslot_str, cur_room_str), CurCourse in self.schedule_dict.items():
            # 如果当前时段有课程安排,则进行判断
            if CurCourse is not None:
                # 同一课程同一时间不能安排在多个教室,同一时间同一课程名代表有冲突
                # 在安排中则代表有冲突
                if (cur_timeslot_str, CurCourse.name_str) in course_time_dict:
                    fitness_float -= 3
                else:
                    # 没有在安排表中，记录此次安排
                    course_time_dict[(cur_timeslot_str, CurCourse.name_str)] = cur_room_str
                    # 安排此课,适应度分值加上优先级分值
                    fitness_float += CurCourse.priority_float
                    # 统计教师被安排的次数
                    teacher_assigned_dict[CurCourse.teacher_str] += 1

                    # 学生不能同时上两门及以上课程,进行冲突检测
                    for CurStudent in self.student_list:
                        if CurCourse in CurStudent.enrolled_courses_list:
                            if cur_timeslot_str in CurStudent.time_slots_list:
                                # 有冲突大幅降低适应度
                                fitness_float -= 3
                                # 记录冲突信息
                                self.conflict_info_list.append((CurStudent.name_str, CurCourse.name_str, cur_timeslot_str))
                            
                            # 更新学生的时间段表,增加此上课时间到学生的上课时间表中
                            else:
                                CurStudent.time_slots_list.append(cur_timeslot_str)

                # 如果此门课程的安排时间在教师不可以上课的时间列表中，适应度大幅降低
                if cur_timeslot_str in CurCourse.unavailable_timeslots_list:
                    fitness_float -= 3

        # 教师排课均衡性评分
        for course_teacher_name_str, teacher_assigned_count in teacher_assigned_dict.items():
            # 教师没有被分配到课程
            if teacher_assigned_count == 0:
                fitness_float -= 5
            # 教师被分配了大于等于3次课程
            elif teacher_assigned_count >= 3:
                fitness_float -= 2
            # 教师排课次数均衡
            else:
                fitness_float += 1

        # 返回适应度
        return fitness_float

    # 基因变异操作
    def mutate(self):
        # 随机选择一个时间段和教室组合
        random_timeslot_room_tuple = random.choice(list(self.schedule_dict.keys()))
        # 随机选择一门课程
        random_new_course_str = random.choice(self.course_list)
        # 替换该位置的课程
        self.schedule_dict[random_timeslot_room_tuple] = random_new_course_str

    # 基因交叉操作
    def crossover(self, other):
        # 随机选择交叉基因的起点
        crossover_index_int = random.randint(0, len(self.schedule_dict) - 1)
        # 初始化两个子代的基因
        child1_schedule_dict = {}
        child2_schedule_dict = {}

        # 迭代所有时间和房间的键值对
        for i, schedule_key_tuple in enumerate(self.schedule_dict.keys()):
            # 子代1交叉基因起点之前的基因来自本个体,子代2的基因来自其他个体
            if i <= crossover_index_int:
                child1_schedule_dict[schedule_key_tuple] = self.schedule_dict[schedule_key_tuple]
                child2_schedule_dict[schedule_key_tuple] = other.schedule_dict[schedule_key_tuple]
            else:
                # 子代1交叉基因起点之后的基因来自其他个体,子代2的基因来自本个体
                child1_schedule_dict[schedule_key_tuple] = other.schedule_dict[schedule_key_tuple]
                child2_schedule_dict[schedule_key_tuple] = self.schedule_dict[schedule_key_tuple]

        # 初始化两个子代类的基因
        Child1Schedule = Schedule(self.course_list, self.timeslots_list, self.room_list, self.student_list)
        Child2Schedule = Schedule(self.course_list, self.timeslots_list, self.room_list, self.student_list)
        # 赋予子代基因
        Child1Schedule.schedule_dict = child1_schedule_dict
        Child2Schedule.schedule_dict = child2_schedule_dict

        # 返回两个新子代基因
        return Child1Schedule, Child2Schedule

    def display(self):
        # 存储未安排课程的教师、学生和教室
        unassigned_teachers = set(teacher.teacher_str for teacher in self.course_list)
        unassigned_rooms = set(self.room_list)
        unassigned_students = set(student.name_str for student in self.student_list)

        # 初始化当前代排课信息字典
        current_generation_info_dict = {
            # 初始化当前代排课信息
            "room_assigned_course_schedule_dict": {},
            # 初始化未安排的教室和时间段
            "unassigned_room_time_list": [],
            # 初始化未安排的教师
            "unassigned_teacher_list": [],
            # 初始化未安排的教室
            "unassigned_room_list": [],
            # 初始化未安排的学生
            'unassigned_student_list': []
        }

        for (cur_timeslot_str, cur_room_str), CurCourse in self.schedule_dict.items():
            # 如果课程为非空,则打印课程信息
            if CurCourse is not None:
                # 初始化本门课的选课学生列表
                enrolled_course_student_name_list = []
                # 遍历学生列表
                for CurStudent in self.student_list:
                    # 如果本门课在当前学生选课列表中,则将学生姓名加入选课学生列表
                    if CurCourse in CurStudent.enrolled_courses_list:
                        enrolled_course_student_name_list.append(CurStudent.name_str)
                        # 从未安排列表中移除学生
                        unassigned_students.discard(CurStudent.name_str)
                enrolled_course_student_str = ", ".join(enrolled_course_student_name_list) if enrolled_course_student_name_list else "No student enrolled"

                # 检查教师是否在不可上课时间
                teacher_unavailable = cur_timeslot_str in CurCourse.unavailable_timeslots_list
                availability_str = " Teacher unavailable during this time" if teacher_unavailable else ""


                # 初始化冲突信息
                conflict_str = ""
                for conflict_info_tuple in self.conflict_info_list:
                    if conflict_info_tuple[1] == CurCourse.name_str and conflict_info_tuple[2] == cur_timeslot_str:
                        conflict_str = f"Conflict: {conflict_info_tuple[0]}"

                # 排课时间、教师、课程名、授课教师、课程优先级、选课学生、冲突信息、不可上课信息
                room_course_schedule_str = f"{cur_timeslot_str} in {cur_room_str}: {CurCourse.name_str} by {CurCourse.teacher_str} (Priority: {CurCourse.priority_float}) | Enrolled: {enrolled_course_student_str}{conflict_str}{availability_str}"
                print(room_course_schedule_str)
                # 添加到字典中,使用课程名作为键,值为排课信息
                current_generation_info_dict["room_assigned_course_schedule_dict"][CurCourse.name_str]={"time":cur_timeslot_str,"room":cur_room_str,"course":CurCourse.name_str,"teacher":CurCourse.teacher_str,"priority":CurCourse.priority_float,"enrolled_student":enrolled_course_student_str,"conflict":conflict_str,"availability":availability_str}

                # 从未安排列表中移除教师和教室
                unassigned_teachers.discard(CurCourse.teacher_str)
                unassigned_rooms.discard(cur_room_str)
            else:
                # 未安排教室和时间段
                unassigned_room_time_str = f"{cur_timeslot_str} in {cur_room_str}: Free"
                # 添加到字典中
                current_generation_info_dict["unassigned_room_time_list"].append(unassigned_room_time_str)
                print(unassigned_room_time_str)

        # 打印未安排的教师、教室和学生
        if unassigned_teachers:
            unassigned_teachers_str = "Unassigned Teachers: " + ", ".join(unassigned_teachers)
        else:
            unassigned_teachers_str = "All teachers assigned."
        # 添加到字典中
        current_generation_info_dict["unassigned_teacher_list"].append(unassigned_teachers_str)
        print(unassigned_teachers_str)

        if unassigned_rooms:
            unassigned_room_str = "Unassigned Rooms: " + ", ".join(unassigned_rooms)
        else:
            unassigned_room_str = "All rooms assigned."
        # 添加到字典中
        current_generation_info_dict["unassigned_room_list"].append(unassigned_room_str)
        print(unassigned_room_str)

        if unassigned_students:
            unassigned_student_str = "Unassigned Students: " + ", ".join(unassigned_students)
        else:
            unassigned_student_str = "All students enrolled."
        # 添加到字典中
        current_generation_info_dict["unassigned_student_list"].append(unassigned_student_str)
        print(unassigned_student_str)

        return current_generation_info_dict

        

# 初始化种群
def initialize_population(course_list, timeslots_list, room_list, student_list, population_size=100):
    # 种群列表初始化
    population_list = []
    for _ in range(population_size):
        # 实例化一个个体
        SingleSchedule = Schedule(course_list, timeslots_list, room_list, student_list)
        # 对个体的基因进行随机初始化
        for schedule_key_tuple in SingleSchedule.schedule_dict.keys():
             # 随机一个基因(对时间段和教室的组合随机选择一门课)
            SingleSchedule.schedule_dict[schedule_key_tuple] = random.choice(course_list)

        # 将初始化后的个体加入种群列表
        population_list.append(SingleSchedule)

    # 返回初始化的种群列表
    return population_list

# 交叉和变异获得下一代种群
def genetic_evolution(population_list,retention_number_int):
    
    # 计算适应度,并对种群列表进行倒序排序
    population_list.sort(key=lambda x: x.fitness(), reverse=True)

    # 初始化下一代个体列表
    next_generation_list = []
    # 保留最优的部分个体
    for i in range(retention_number_int):
        next_generation_list.append(population_list[i])

    # 选择和交叉,直到达到种群大小
    while len(next_generation_list) < len(population_list):
        # 随机在适应度最高的部分中选择父母
        parent1 = random.choice(population_list[:10])
        parent2 = random.choice(population_list[:10])
        # 对父母基因进行交叉,得到两个子代
        child1, child2 = parent1.crossover(parent2)
        # 将两个子代加入下一代个体列表
        next_generation_list.append(child1)
        next_generation_list.append(child2)

    # 子代和父代有概率变异
    for ChildsChedule in next_generation_list:
        if random.random() < 0.3:
            ChildsChedule.mutate()

    return next_generation_list

# 渲染前端页面的路由
@router.get("/course_schedule")
async def course_schedule(request: Request):
    return TemplatesJinja2CourseSchedule.TemplateResponse("course_schedule.html", {"request": request})

# 开始排课
@router.websocket("/ws_course_schedule")
async def ws_course_schedule(websocket: WebSocket):
  
    # 示例课程（课程名、任课教师、课时长(单位小时)、优先级(数字越高优先级越高)、不可上课时间）
    course_list = [
        Course(
            name_str="class1", teacher_str='teacher1', duration_float=1, 
            priority_float=1, unavailable_timeslots_list=["time2", "time4"]
            ),
    ]
    
    # 生成课程样本
    course_list = []
    teachers = [f'teacher{i}' for i in range(1, 21)]
    for i in range(1, 101):  # 生成100门课程
        unavailable_timeslots = random.sample(["time1", "time2", "time3", "time4", "time5", "time6"], random.randint(0, 2))
        course_list.append(Course(
            name_str=f'class{i}',
            teacher_str=random.choice(teachers),
            duration_float=random.uniform(1, 3),  # 课时长为1到3小时
            priority_float=random.randint(1, 3),  # 优先级为1到3
            unavailable_timeslots_list=unavailable_timeslots
        ))

    # 生成时间段和教室
    timeslots_list = ["time1", "time2", "time3", "time4", "time5", "time6"]
    timeslots_list = [f'time{i}' for i in range(1,7)]
    room_list = [f'Room{i}' for i in range(1, 31)]

    # 生成学生样本
    student_list = [Student(f'student{i}') for i in range(1, 101)]  # 生成100个学生

    # 学生选课
    for student in student_list:
        courses_to_enroll = random.sample(course_list, random.randint(1, 5))  # 随机选择1到5门课程
        for course in courses_to_enroll:
            student.enroll(course)


    # 种群大小和适应度阈值
    population_size_int = 100
    fitness_threshold_float = 500
    # 保留最优的多少个
    retention_number_int=5

    # 获得初始化的种群
    PopulationList = initialize_population(course_list, timeslots_list, room_list, student_list, population_size_int)

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
        print(f"Generation {generation_int}: Best Fitness = {best_fitness_float}")
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
        if best_fitness_float >= fitness_threshold_float:
            break

    # print(f"best_fitness_float:{best_fitness_float},Final Best Schedule:")
    # 将内容发送给前端实时显示
    # await websocket.send_json({"generation": generation_int,"best_fitness":best_fitness_float})
    # best_schedule.display()

if __name__ == "__main__":
    # 示例课程（课程名、任课教师、课时长(单位小时)、优先级(数字越高优先级越高)、不可上课时间）
    course_list = [
        Course(
            name_str="class1", teacher_str='teacher1', duration_float=1, 
            priority_float=1, unavailable_timeslots_list=["time2", "time4"]
            ),
    ]
    
    # 生成课程样本
    course_list = []
    teachers = [f'teacher{i}' for i in range(1, 21)]
    for i in range(1, 101):  # 生成100门课程
        unavailable_timeslots = random.sample(["time1", "time2", "time3", "time4", "time5", "time6"], random.randint(0, 2))
        course_list.append(Course(
            name_str=f'class{i}',
            teacher_str=random.choice(teachers),
            duration_float=random.uniform(1, 3),  # 课时长为1到3小时
            priority_float=random.randint(1, 3),  # 优先级为1到3
            unavailable_timeslots_list=unavailable_timeslots
        ))

    # 生成时间段和教室
    timeslots_list = ["time1", "time2", "time3", "time4", "time5", "time6"]
    timeslots_list = [f'time{i}' for i in range(1,7)]
    room_list = [f'Room{i}' for i in range(1, 31)]

    # 生成学生样本
    student_list = [Student(f'student{i}') for i in range(1, 101)]  # 生成100个学生

    # 学生选课
    for student in student_list:
        courses_to_enroll = random.sample(course_list, random.randint(1, 5))  # 随机选择1到5门课程
        for course in courses_to_enroll:
            student.enroll(course)


    # 种群大小和适应度阈值
    population_size_int = 100
    fitness_threshold_float = 500
    # 保留最优的多少个
    retention_number_int=5

    # 获得初始化的种群
    population_list = initialize_population(course_list, timeslots_list, room_list, student_list, population_size_int)

    # 初始化进化次数
    generation_int = 0
    while True:
        # 交叉和变异获得下一代种群
        population_list = genetic_evolution(population_list,retention_number_int)

        # 获取最优个体
        best_schedule = max(population_list, key=lambda x: x.fitness())
        best_fitness_float = best_schedule.fitness()

        # 打印当前代的最优适应度
        generation_int += 1
        print(f"Generation {generation_int}: Best Fitness = {best_fitness_float}")
        best_schedule.display()
        print("-" * 40)

        # 如果达到了适应度要求，退出循环
        if best_fitness_float >= fitness_threshold_float:
            break

    print(f"best_fitness_float:{best_fitness_float},Final Best Schedule:")
    best_schedule.display()

    # import uvicorn
    # uvicorn.run(app="route_course_schedule:app", host="0.0.0.0", port=8000, reload=True)

