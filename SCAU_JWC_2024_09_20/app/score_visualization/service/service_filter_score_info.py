'''
Author: xudawu
Date: 2024-10-24 14:48:41
LastEditors: xudawu
LastEditTime: 2024-10-25 16:19:34
'''
import collections
from app.score_visualization.database import database_score
from app.score_visualization import public_function

# 获得所有学院班级字典
def get_all_college_class_dict():
    '''
    数据格式要求：
    student_id_str:
        学生学号,字符串类型
    row_list:
        行数据列表,列表类型，每一行是一个类对象
        一个对象包含成绩信息,学期和班级信息应当固定为特定的一个学期和特定班级,本函数不区分学期和班级，只区分学号
    预期的row_list为:
        某个学期某个班的所有学生的成绩
    返回数据：
        此学生的成绩列表,列表类型,一维列表,列表内的元素为一个学生的成绩
    '''
    # 获得所有有成绩的班级列表
    class_list = get_all_have_score_class_list()

    # 初始化学院班级字典
    # 创建一个 defaultdict,自动处理缺失和重复的键
    college_class_dict = collections.defaultdict(list)

    # 执行sql语句,返回执行标志和执行数据
    excute_sql_flag_str,excute_count_int,rows = database_score.get_all_college_class()
    # 遍历列表并赋值到字典中
    for TempRow in rows:
        # 只存储有成绩的班级
        class_name_str = TempRow.班级
        if class_name_str in class_list:
            college_class_dict[TempRow.学院].append(class_name_str)

    # 将 defaultdict 转换为普通字典
    college_class_dict = dict(college_class_dict)

    # 返回学院班级字典
    return college_class_dict

# 获得成绩表中有成绩的班级列表
def get_all_have_score_class_list():
    '''
    数据格式要求：
    student_id_str:
        学生学号,字符串类型
    row_list:
        行数据列表,列表类型，每一行是一个类对象
        一个对象包含成绩信息,学期和班级信息应当固定为特定的一个学期和特定班级,本函数不区分学期和班级，只区分学号
    预期的row_list为:
    '''
    # 学院班级列表数据
    excute_sql_flag_str,excute_count_int,rows = database_score.get_all_have_score_class_list()
    # 列表推导式获得班级列表
    class_list = [item[0] for item in rows]

    # 返回班级列表
    return class_list


# 获得班级有的课程类型名称列表
def get_all_have_score_course_type_by_class(class_name_str):
    '''
    数据格式要求：
    class_name_str:
        班级名称,字符串类型
        示例：
        class_name_str = '农学202001'
    返回数据：
        此班级有成绩的课程类型列表
        示例：
        course_type_list = ['必修', '公共选修课', '其他选修课', '实践教学', '推荐选修课', '专业方向课', '专业拓展课']
    '''
    excute_sql_flag_str,excute_count_int,rows = database_score.get_all_course_type_by_class(class_name_str)
    # 去掉元组嵌套
    course_type_list = public_function.remove_tuple_nest(rows)

    # 返回课程类型列表
    return course_type_list

if __name__ == '__main__':
    # 引入文件目录设置
    import sys
    import os
    # 添加项目文件根目录到系统路径
    module_path = os.path.abspath('SCAU_JWC_2024_09_20')
    sys.path.append(module_path)

    # 引入模板文件
    from app.template import TemplatesJinja2ScoreVisualization
    from app.score_visualization.database import database_score
    from app.score_visualization import public_function

    # 查询测试
    class_name_str = '农学202001'
    course_type_name = '必修'
    # 学期
    semester_list = ['2022-2023-1','2022-2023-2','2023-2024-1','2023-2024-2']

    # 获得所有有成绩的班级列表
    # college_class_dict = get_all_college_class_dict()
    # print(len(college_class_dict))

    course_type_list = get_all_have_score_course_type_by_class(class_name_str)
    print(course_type_list)