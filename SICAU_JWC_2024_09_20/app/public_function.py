'''
Author: xudawu
Date: 2024-10-25 14:14:57
LastEditors: xudawu
LastEditTime: 2024-10-29 12:06:48
'''

# 学期升序排序
def sort_semester_list(semester_list):
    '''
    输入数据格式要求：
    semester_list:
        学期列表,字符串类型
        示例：
        [('2023-2024-1',), ('2023-2024-2',), ('2022-2023-1',)]
    返回数据：
    sorted_semester_list:
        升序排序后的学期列表,列表类型
        示例：
        ['2022-2023-1', '2023-2024-1', '2023-2024-2']
    '''
    # 定义排序的关键函数
    def sort_key(semester_str):
        year, _, term = semester_str.split('-')
        return (int(year), int(term))

    # 使用 sorted 函数进行排序
    sorted_semester_list = sorted(semester_list, key=sort_key)

    # 返回排序后的学期列表
    return sorted_semester_list

# 获取二维列表最小值和最大值
def get_min_max_in_list(data_list):
    '''
    输入数据格式要求：
    data_list:
        成绩列表,第一位为分类标记,第二位为学号,后面为成绩
        示例：
        [
            [2, '202000017', 88.5, 84.375, 88.0, 86.6, 85.14285714285714, 82.4, 64.5],
            [3, '202000018', 88.5, 84.375, 88.0, 86.6, 85.14285714285714, 82.4, 64.5],
            [1, '202000019', 88.5, 84.375, 88.0, 86.6, 85.14285714285714, 82.4, 64.5],
        ]
    返回数据：
    min_value,max_value:
        整个列表的最小值、最大值
        示例：
            64.5,88.5
    '''
    min_value = float('inf')
    max_value = float('-inf')

    for row in data_list:
        for value in row[2:]:
            # 跳过空值
            if value is None:
                continue
            # 更新最小值和最大值
            if value < min_value:
                min_value = value
            if value > max_value:
                max_value = value

    return min_value, max_value

# 去掉列表内的元组嵌套
def remove_tuple_nest(input_list):
    '''
    输入数据格式要求：
    input_list:
        输入列表,列表类型,列表内的元素为元组
        示例：
        [('必修',), ('公共选修课',), ('其他选修课',), ('实践教学',), ('推荐选修课',), ('专业方向课',), ('专业拓展课',)]
    返回数据：
    output_list:
        输出列表,列表类型,列表内的元素为字符串
        示例：
        ['2023-2024-1', '2023-2024-2', '2022-2023-1']
    '''
    # 使用列表推导式去除元组嵌套
    output_list = [item[0] for item in input_list]

    return output_list

# 字典内部的列表按年级排序
def sort_dict_by_list_value(dict_data):
    '''
    输入数据格式要求：
    dict_data:
        字典数据,键为字符串类型,值为列表类型
        示例：
        {
            '体育学院': ['体育201601', '体育教育201602', '体育201701'], 
            '生命科学学院': ['生工201505', '生物201601', '生物201602', '生物201603'], 
            '林学院': ['产品设计201601', '产品设计201602', '森林保护201701', '木科201702']
        }
    返回数据：
    原地修改字典不返回数据,返回字典内部列表按后6位数升序排序的列表:
        示例：
        ['2023-2024-1', '2023-2024-2', '2022-2023-1']
    '''
    # 遍历字典的键值对，将值转换为列表
    for key, value in dict_data.items():
        
        # 原地改造原字典的列表
        # 按后6位数字降序排序
        dict_data[key]  = sorted(dict_data[key], key=lambda x: x[-6:],reverse=True)

# 获取列表平均分
def get_average_from_list(score_list):
    # 去掉 None 值
    pure_score_list = [score for score in score_list if score is not None]

    # 计算平均分
    # 确保列表不为空
    if len(pure_score_list)!=0:
        avg_float = sum(pure_score_list) / len(pure_score_list)
    else:
        avg_float=None
    # 返回平均分
    return avg_float