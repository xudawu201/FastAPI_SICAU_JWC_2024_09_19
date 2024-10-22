'''
Author: xudawu
Date: 2024-10-22 08:18:10
LastEditors: xudawu
LastEditTime: 2024-10-22 08:18:30
'''
import pandas
import plotly
import math

# 读取 Excel 文件
def read_excel_data(file_path):
    print(f'加载文件：{file_path}')
    return pandas.read_excel(file_path)

# 获取成绩数据
def get_scores(dataframe, college_name, course_type_name):
    print(f'提取{college_name}的{course_type_name}数据')
    student_score = []
    temp_score = []
    # 临时学生列表
    temp_student_number_list = []
    student_select_info = '学号'
    # 班级名称
    class_column_name = '班级'
    # 班主任名字
    class_teacher_column_name = '班主任名字'
    # 使用 loc 遍历 DataFrame 的每一行
    for i in range(len(dataframe)):
        student_info = dataframe.loc[i]  # 使用 loc 根据行标签访问数据

        # 跳过非指定学院的学生
        if student_info['学院'] != college_name:
            continue
        # 跳过已记录成绩的学生,用学号匹配
        if student_info[student_select_info] in temp_student_number_list:
            continue
        # 锁定此学号
        temp_student_numer= student_info[student_select_info]
        # 记录此学号
        temp_student_number_list.append(temp_student_numer)
        # 添加学生类别
        temp_score.append(student_info['学生按高考成绩划分三档(123分别代表前1/3、中1/3、后1/3)'])
        # 添加高考成绩
        temp_score.append(student_info['高考成绩百分制'])
        # 获得此学号的所有成绩
        for j in range(len(dataframe)):
            # 获得这一行的数据
            temp_student_infor = dataframe.loc[j]
            # 匹配学号
            if temp_student_infor['学号'] == temp_student_numer:
                # 添加成绩
                temp_score.append(temp_student_infor[course_type_name])

        print(f'成功提取{student_select_info}:{temp_student_numer}的{course_type_name}数据')
        # 添加到整体成绩数据中
        student_score.append(temp_score)

        # 记录班级和班主任名字
        class_name = student_info[class_column_name]
        class_teacher_name = student_info[class_teacher_column_name]
        
        # 清空临时列表
        temp_score = []

    # 学生人数
    student_count_int = len(student_score)
    print(f'成功提取{class_name}:{student_count_int}名学生的成绩数据')
    return class_name,class_teacher_name,student_count_int,student_score

# 获取二维列表最小值和最大值
def get_min_max_in_list(data_list):
    min_value = float('inf')
    max_value = float('-inf')

    for row in data_list:
        for value in row[1:]:
            # 跳过空值
            if pandas.isnull(value):
                continue
            if value < min_value:
                min_value = value
            if value > max_value:
                max_value = value

    return min_value, max_value

# 去掉列表中的None值并排序
def get_sorted_list(data_list):
    # 分离 None 值
    none_count = data_list.count(None)
    numbers_only = [x for x in data_list if x is not None]

    # 排序数字
    numbers_only_sorted = sorted(numbers_only,reverse=True)

    # 合并排序后的数字和 None,将None值替换为0
    sorted_list_with_none = numbers_only_sorted + ([0] * none_count)

    return sorted_list_with_none

# 获得分类标准线数据
def get_standard_line(student_count_int,student_score_list):
    
    # 高考成绩列表
    gaokao_score_list = []
    # 前30%标准线
    top_30_percent_score_list = []
    # 前70%标准线
    top_70_percent_score_list = []
    # 学年成绩
    score_year1=[]
    score_year2=[]
    score_year3=[]
    score_year4=[]
    for temp_score in student_score_list:
        # 高考成绩
        gaokao_score_list.append(temp_score[1])
        # 学年成绩
        score_year1.append(temp_score[2])
        score_year2.append(temp_score[3])
        score_year3.append(temp_score[4])
        score_year4.append(temp_score[5])
    
    # 对成绩列表进行降序排序（分数越高排名越前）
    gaokao_score_list = get_sorted_list(gaokao_score_list)
    
    # 学年成绩排序
    score_year1 = get_sorted_list(score_year1)
    score_year2 = get_sorted_list(score_year2)
    score_year3 = get_sorted_list(score_year3)
    score_year4 = get_sorted_list(score_year4)

    # 计算前30%和前70%的位置
    top_30_percent_index = int(student_count_int * 0.3)
    top_70_percent_index = int(student_count_int * 0.7)

    # 先添加前30%和前70%的学年成绩
    top_30_percent_score_list.append(gaokao_score_list[top_30_percent_index])
    top_70_percent_score_list.append(gaokao_score_list[top_70_percent_index])

    # 添加标准线数据
    top_30_percent_score_list.append(score_year1[top_30_percent_index])
    top_70_percent_score_list.append(score_year1[top_70_percent_index])

    top_30_percent_score_list.append(score_year2[top_30_percent_index])
    top_70_percent_score_list.append(score_year2[top_70_percent_index])

    top_30_percent_score_list.append(score_year3[top_30_percent_index])
    top_70_percent_score_list.append(score_year3[top_70_percent_index])

    top_30_percent_score_list.append(score_year4[top_30_percent_index])
    top_70_percent_score_list.append(score_year4[top_70_percent_index])
        
    # 返回前30%和前70%的标准线
    return top_30_percent_score_list,top_70_percent_score_list

# 线条设置
def create_traces(student_score_list,top_30_percent_score_list,top_70_percent_score_list):
    # 轨迹列表
    traces = []
    name_list = ['排名前1/3学生成绩平均值', '排名中间1/3学生成绩平均值', '排名后1/3学生成绩平均值']
    # x 轴值，与每组 y 的长度一致
    x_value = [0, 1, 2, 3, 4]
    # 颜色列表
    color_list = ['green', 'blue', 'red']
    show_legend = {
        color_list[0]: True,  # 对应绿色分组
        color_list[1]: True,  # 对应蓝色分组
        color_list[2]: True   # 对应红色分组
    }
    
    # 添加成绩线
    # 遍历 y_values 创建数据线
    for i, y in enumerate(student_score_list):
        # 根据第一个数据的值设置颜色
        if y[0] == 1:
            # color = 'green'  # 绿色
            color = color_list[0]  # 绿色
            name = '入学成绩班级前30%'
            legendgroup = 'green_group'
            legendrank=1
        elif y[0] == 2:
            # color = 'blue'   # 蓝色
            color = color_list[1]   # 蓝色
            name = '入学成绩班级中间40%'
            legendgroup = 'blue_group'
            legendrank=2
        else:
            # color = 'red'    # 红色
            color = color_list[2]    # 红色
            name = '入学成绩班级后30%'
            legendgroup = 'red_group'
            legendrank=3

        trace = plotly.graph_objs.Scatter(
            x=x_value,  # 使用固定长度的 x_values
            y=y[1:],  # 正确的 y 数据
            mode='lines+markers',
            name=name,
            # line=dict(color=color,dash='dash'),  # 设置线条颜色、线型
            line=dict(color=color,dash='solid'),  # 设置线条、线型
            # opacity=0.5,  # 设置透明度
            showlegend=show_legend[color],  # 控制图例显示
            legendgroup=legendgroup,  # 同一组图例
            legendrank=legendrank  # 设置图例顺序
        )
        traces.append(trace)

        # 图例只显示一次
        show_legend[color] = False

    # 创建前30%和前70%成绩的标准线
    standard_traces = [
        plotly.graph_objs.Scatter(
            x=[0, 1, 2, 3, 4],  # x 轴值，与每组 y 的长度一致
            y=top_30_percent_score_list,  # 创建水平线，y值是前30%成绩
            mode='lines',
            name='班级前30%成绩基准线',
            # line=dict(color='black', dash='solid'),  # 使用黑色实线
            line=dict(color='rgb(246,193,77)', dash='dot'),  # 使用橙色点线
            showlegend=True
        ),
        plotly.graph_objs.Scatter(
            x=[0, 1, 2, 3, 4],  # x 轴值，与每组 y 的长度一致
            y=top_70_percent_score_list,  # 创建水平线，y值是前70%成绩
            mode='lines',
            name='班级前70%成绩基准线',
            # line=dict(color='black', dash='solid'),  # 使用实线
            line=dict(color='rgb(0,0,0)', dash='dot'),  # 使用黑色点线
            showlegend=True
        )
    ]

    # 将标准线添加到 traces 列表中
    traces.extend(standard_traces)
    
    return traces

# 坐标轴、图例等设置
def get_layout(traces, college_name, class_name, course_type_name, student_count_int, class_teacher_name, y_axis_range, width, height, y_axis_dtick):
    layout = plotly.graph_objs.Layout(
        title={
            'text': f"{college_name}_{class_name}_{course_type_name}_成绩走势图<br><sub>班级人数: {student_count_int}  班主任姓名: {class_teacher_name}</sub>",
            'x': 0.5,
            'xanchor': 'center'
        },
        plot_bgcolor='white',paper_bgcolor='white',
        xaxis=dict(
            title='学年',showgrid=False,zeroline=True,showline=True,linecolor='black',
            rangemode='tozero',dtick=1,range=[0, 4],
            tickvals=[0, 1, 2, 3, 4],
            ticktext=['入学成绩折算分数（百分制）', '第1学年', '第2学年', '第3学年', '第4学年']
        ),
        yaxis=dict(
            title='平均成绩',showgrid=True,zeroline=True,showline=True, linecolor='black',gridcolor='lightgrey',
            rangemode='tozero',range=[y_axis_range[0], y_axis_range[1]],
            dtick=y_axis_dtick,
        ),
        width=width,
        height=height,
        # 图例加背景框
        legend=dict(
            x=1.05, y=1, traceorder='normal', font=dict(size=10),
            bgcolor='rgba(255, 255, 255, 0)', bordercolor='Black', borderwidth=1
        )
    )

    return layout

# 获得单个学院的班级数据
def college_student_score(college_name,course_type_name,dataframe):
    
    # 获得班级名,班主任名,学生人数和班级成绩列表
    class_name,class_teacher_name,student_count_int,student_score_list = get_scores(dataframe, college_name, course_type_name)
    
    # 获得前30%和前70%成绩的标准线
    top_30_percent_score_list,top_70_percent_score_list = get_standard_line(student_count_int,student_score_list)

    # 获取分数的最小值和最大值,用于自动确定y轴的范围
    min_value, max_value = get_min_max_in_list(student_score_list)
    # 计算y轴的范围，最小值减2，最大值加2
    y_axis_range = [min_value - 2, max_value + 2]
    # 图像宽度和高度
    width = 1000
    height = 600
    # y轴的刻度
    y_axis_dtick = 1
    
    # 创建轨迹，用于展示分数分布
    traces = create_traces(student_score_list,top_30_percent_score_list,top_70_percent_score_list)
    
    # 创建布局，设置图表的标题、y轴标签、图例等
    layout_plotly = get_layout(traces, college_name, class_name, course_type_name, student_count_int, class_teacher_name, y_axis_range, width, height, y_axis_dtick)

    # 创建图表，并设置数据和布局
    fig_plotly = plotly.graph_objs.Figure(data=traces, layout=layout_plotly)

    # 将图表保存为图片
    file_name = f'{college_name}_{class_name}_{course_type_name}.png'
    plotly.io.write_image(fig_plotly, file_name)

    print(f'成功保存{file_name}图片')

def main():
    excel_path = 'Asset2021_10_23\\学生成绩平均分_高考成绩_班主任_高考成绩分类_2020级_2024_09_18.xlsx'
    college_name = '农学院'
    course_type_name = '必修平均分'
    
    # 加载Excel文件
    dataframe = read_excel_data(excel_path)
    
    # 获得单个学院的成绩图
    # college_student_score(college_name,course_type_name,dataframe)

    # 获得所有学院的成绩图
    college_name_list = []
    for i in range(len(dataframe)):
        # 获得一行
        dataframe_row = dataframe.loc[i]
        
        # 锁定学院
        if dataframe_row['学院'] not in college_name_list:
            temp_college_name = dataframe_row['学院']
            college_name_list.append(temp_college_name)

            # 获得单个学院的成绩图
            college_student_score(temp_college_name,course_type_name,dataframe)

'''
读取excel文件中的学生成绩数据,按高考成绩排序将学生划分为3类
分别为前1/3,中1/3,后1/3,分别计算每一个学生的平均分,然后按学生所属的类别赋予线条颜色绘制成绩走势图
并做两条标准线,分别为每学年前30%和前70%平均分的标准线
'''
if __name__ == '__main__':
    
    main()
