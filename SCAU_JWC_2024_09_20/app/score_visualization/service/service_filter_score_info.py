'''
Author: xudawu
Date: 2024-10-24 14:48:41
LastEditors: xudawu
LastEditTime: 2024-10-24 15:00:09
'''
from app.score_visualization.database import database_score

def get_all_score_info():
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
    excute_sql_flag_str,excute_count_int,rows = database_score.get_all_college()
    # 学生成绩表
    # student_score_list = []
    # for TempRow in rows:
    #     # 学号
    #     if student_id_str == TempRow.学号:
    #         # 成绩
    #         score_float = TempRow.成绩
    #         # 成绩列表
    #         student_score_list.append(score_float)
    return rows

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

    # 查询测试
    class_name_str = '农学202001'
    course_type_name = '必修'
    # 学期
    semester_list = ['2022-2023-1','2022-2023-2','2023-2024-1','2023-2024-2']

    excute_sql_flag_str,excute_count_int,rows = database_score.get_all_college()
    print(rows)