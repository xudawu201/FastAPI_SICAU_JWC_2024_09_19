'''
Author: xudawu
Date: 2024-10-21 15:35:21
LastEditors: xudawu
LastEditTime: 2024-11-22 16:35:29
'''
import plotly
import copy
import math

# 引入自定义文件
from app.score_visualization.database import database_score
from app import public_function

# 获得学生的成绩
def get_student_score_by_id(student_id_str,row_list):
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
    # 学生成绩表
    student_score_list = []
    for TempRow in row_list:
        # 学号
        if student_id_str == TempRow.学号:
            # 成绩
            score_float = TempRow.成绩
            # 成绩列表
            student_score_list.append(score_float)
    return student_score_list

# 获得平均分
def get_average_score(score_list):
    '''
    数据格式要求：
    score_list:
        学生成绩列表,列表类型,一维列表,列表内的元素为一个学生的成绩
    返回数据：
        此列表的平均分,浮点数类型
    '''
    # 初始化成绩列表,深拷贝
    temp_score_list = copy.deepcopy(score_list)
    # 初始化平均分成绩列表
    average_class_student_score_list=[]

    # 去掉子列表的第一位学号再计算平均分
    for temp_list in temp_score_list:
        # 记录学号
        average_class_student_score_list.append([temp_list[0]])
        # 去掉学号
        temp_list.pop(0)

    # 计算平均分
    student_index_int = 0
    for temp_temp_score_list in temp_score_list:
        # 初始化平均成绩
        average_score_float = None
        # 去掉None成绩
        temp_temp_score_list = [item for item in temp_temp_score_list if item is not None]
        # 如果有成绩再计算平均分
        if len(temp_temp_score_list) != 0:
            average_score_float = sum(temp_temp_score_list) / len(temp_temp_score_list)
        
        # 判断是否有数据
        if average_score_float != None:
            # 存入平均分
            average_class_student_score_list[student_index_int].append(average_score_float)

        # 索引增加
        student_index_int += 1

    return average_class_student_score_list

# 获得降序排序的成绩列表
def get_sorted_list_desc(score_list):
    '''
    数据格式要求：
    score_list:
        学生成绩列表,列表类型,二维列表,列表中的列表内元素为一个学生的成绩
    返回数据：
        此列表的降序排序,列表类型,一维列表,列表内的元素为一个学生的成绩
    '''
    # 初始化成绩列表,用于存储学生
    temp_scores_list = []
    for temp_this_score_list in score_list:
        
        # 从此学生的第一次有成绩开始算,从1开始,跳过学号
        for temp_this_score in temp_this_score_list[1:]:

            if temp_this_score == None :
                continue

            # 记录成绩
            temp_scores_list.append(temp_this_score)
            # 跳过后面的成绩
            break

    # 对成绩列表进行降序排序（分数越高排名越前）
    temp_scores_list.sort(reverse=True)

    # 返回降序排序的成绩列表
    return temp_scores_list

# 获得前30%和前70%的成绩标准线
def get_top_30_percent_and_70_percent_score(student_score_list):
    '''
    数据格式要求：
    average_class_student_score_list:
        成绩列表,二维列表,子列表内元素代表成绩
    返回数据：
        两个成绩,分别为成绩前30%或前70%的成绩基准成绩
    '''
    # 初始化成绩列表,用于存储学生
    temp_scores_list = get_sorted_list_desc(student_score_list)
    
    # 计算列表长度
    student_sum_int = len(temp_scores_list)

    # 计算前30%和前66%的位置,向下取整
    top_30_percent_index = math.floor(student_sum_int * 0.3)
    top_70_percent_index = math.floor(student_sum_int * 0.7)

    # 截取前30%和前70%的成绩
    top_30_percent_score_float = temp_scores_list[top_30_percent_index]
    top_70_percent_score_float = temp_scores_list[top_70_percent_index]

    # 返回成绩
    return top_30_percent_score_float,top_70_percent_score_float

# 给成绩表添加分类标记
def add_student_score_classify(score_list):
    '''
    数据格式要求：
    score_list:
        一个班级的学生成绩表,列表类型,二维列表,子列表内第一个元素为学号，其他的元素为成绩
    返回数据：
        一个班级的学生成绩表,列表类型,二维列表,列表内的元素为一个学生的成绩列表,子列表内的第一个元素为一个学生的分类标记
        1代表前30%的学生,2代表中间40%的学生,3代表后30%的学生

    '''
    # 获得前30%和前70%的成绩点
    top_30_percent_score_float,top_70_percent_score_float = get_top_30_percent_and_70_percent_score(score_list)

    # 根据给班级学生添加标记
    index_int=0
    # 初始化拷贝列表,使用深拷贝使两个列表互不影响
    score_copy_list = copy.deepcopy(score_list)
    # 遍历成绩列表
    for temp_this_score_list in score_list:
        # 初始化成绩
        temp_score_float = None
        # 从此学生的第一次有成绩开始算,从1开始,跳过学号
        for temp_this_score in temp_this_score_list[1:]:

            # 跳过None的成绩
            if temp_this_score == None :
                continue

            # 记录成绩
            temp_score_float = temp_this_score
            # 跳过后面的成绩
            break

        # 如果是无成绩
        if temp_score_float == None:
            score_copy_list[index_int].insert(0, '无成绩')
            index_int += 1
            continue
        # 如果是班级前3/1,分别标记
        if temp_score_float >= top_30_percent_score_float:
            score_copy_list[index_int].insert(0, 1)
        # 如果是中等
        elif temp_score_float >= top_70_percent_score_float:
            score_copy_list[index_int].insert(0, 2)
        else:
            score_copy_list[index_int].insert(0, 3)
        # 索引增加
        index_int += 1
        
    # 返回等级标记和成绩
    return score_copy_list

# 获得以学号分组的所有成绩
def get_student_score_group(row_list):
    '''
    数据格式要求：
    class_name_str:
        班级名称,字符串类型
    row_list:
        行数据列表,列表类型，每一行是一个类对象
        一个对象包含成绩信息,学期信息应当固定为特定的一个学期,本函数不区分学期，只区分班级
    预期的row_list为:
        某个学期所有学生的成绩,学院信息可特定或不特定
    返回数据：
        此班级的学生成绩表,列表类型,二维列表,第一个列表中的列表代表特定学期学生的学号和成绩
        例如：
        [
            [学号,学生1的2020-2021-1成绩1,学生1的2020-2021-1成绩2],
            [学号,学生2的2020-2021-2成绩],
            [学号,学生3的2023-2021-1成绩],
        ]
    '''

    # 学号索引表
    student_id_index_dict = {}
    # 初始化学生学号表
    student_id_list = []
    # 初始化学生成绩表
    class_student_score_list = []
    # 初始化学生索引号
    student_id_index_int = 0
    # 遍历行数据，获得学生学号和索引对应关系
    for TempRow in row_list:
        # 锁定学号
        student_id_str = TempRow.学号
        # 记录不重复的学号
        if student_id_str not in student_id_list:
            # 更新已记录的学号列表
            student_id_list.append(student_id_str)
            # 学号索引字典更新
            student_id_index_dict[student_id_str] = student_id_index_int
            # 学号索引增加
            student_id_index_int += 1  
            # 成绩表先添加学号
            class_student_score_list.append([student_id_str])
    
    # 遍历行数据
    for TempRow in row_list:
        # 锁定学号
        student_id_str = TempRow.学号
        # 获得学号索引
        student_id_index_int = student_id_index_dict[student_id_str]
        # 成绩
        score_float = TempRow.成绩

        # 存入成绩
        class_student_score_list[student_id_index_int].append(score_float)
    
    # 返回学生成绩表
    return class_student_score_list

# 获得指定班级,指定学期,指定课程类型的成绩折线图
def get_score_simple_semester(class_name_str,course_type_str,semester_str):
    '''
    数据格式要求：
    class_name_str:
        班级名称,字符串类型
    course_type_str:
        课程类型,字符串类型
    semester_str:
        学期,字符串类型
    返回数据：
        此班级的学生成绩表,列表类型,二维列表,列表内的元素为一个学生的成绩列表,子列表内的第一个元素为一个学生的分类标记
        1代表前30%的学生,2代表中间40%的学生,3代表后30%的学生
    '''
    # 执行sql语句,返回执行标志和执行数据
    excute_sql_flag_str,excute_count_int,rows = database_score.get_score_database(class_name_str,course_type_str,semester_str)

    # 获得以学号分组的成绩
    class_student_score_list = get_student_score_group(rows)

    # 获得平均分
    average_class_student_score_list = get_average_score(class_student_score_list)
    
    # 获得前30%和前70%的成绩标准线
    top_30_percent_score_float,top_70_percent_score_float = get_top_30_percent_and_70_percent_score(average_class_student_score_list)
    
    # 返回数据
    return average_class_student_score_list,top_30_percent_score_float,top_70_percent_score_float

# 获得多个学期的数据
def get_score_by_semester(class_name_str,course_type_name):

    # 执行sql语句,返回执行标志和执行数据,并获得学期列表
    excute_sql_flag_str,excute_count_int,rows = database_score.get_all_semester_by_class_and_course_type(class_name_str,course_type_name)

    # 去掉元组嵌套
    semester_list = public_function.remove_tuple_nest(rows)

    # 对学期列表进行升序排序
    order_semester_list = public_function.sort_semester_list(semester_list)

    # 初始化数据
    semester_average_class_student_score_list=[]
    baseline_list =[[],[]]
    # 初始化学号字典
    student_id_dict={}
    # 初始化学生索引
    student_index_int=0
    # 初始化学期计数
    semester_count_int=0
    # 遍历学期列表
    for semester_str in order_semester_list:
        # 获得班级成绩
        average_class_student_score_list,top_30_percent_score_float,top_70_percent_score_float = get_score_simple_semester(class_name_str,course_type_name,semester_str)
        
        # 添加前30%和前70%的成绩标准线
        baseline_list[0].append(top_30_percent_score_float)
        baseline_list[1].append(top_70_percent_score_float)

        # 初始化当前学期的学生列表
        cur_semester_student_id_dict = []

        # 根据学号定位到学生的成绩,并添加到列表中
        for student_score_list in average_class_student_score_list:
            # 学号
            student_id_str = student_score_list[0]
            # 记录当前学期的学号
            cur_semester_student_id_dict.append(student_id_str)
            # 成绩
            score_float = student_score_list[1]

            # 如果是首次出现的学号
            if student_id_str not in student_id_dict:
                # 更新学号索引字典
                student_id_dict[student_id_str] = student_index_int
                # 索引增加
                student_index_int += 1

                # 初始化学生成绩列表
                temp_list = [student_id_str]

                # 补足之前的学生成绩
                for i in range(semester_count_int):
                    temp_list.append(None)

                # 存入成绩
                temp_list.append(score_float)

                # 列表末尾存入学号和成绩
                semester_average_class_student_score_list.append(temp_list)

            else:
                # 不是首次出现的学号,定位到学生的成绩
                index_int = student_id_dict[student_id_str]
                semester_average_class_student_score_list[index_int].append(score_float)

        # 处理当前学期没有成绩的学生,将其成绩填充为None
        for student_id_str in student_id_dict.keys():
            # 如果学号不在当前学期的学生列表中
            if student_id_str not in cur_semester_student_id_dict:
                # 定位到学生的成绩
                index_int = student_id_dict[student_id_str]
                # 添加None到成绩占位
                semester_average_class_student_score_list[index_int].append(None)

        # 学期计数增加1
        semester_count_int += 1

    # 添加分类标记
    tag_semester_class_student_average_score_list_list = add_student_score_classify(semester_average_class_student_score_list)
    # 学生人数
    student_count_int = len(student_id_dict)
    # print(f'学生人数：{student_count_int}')
    # 返回数据
    return tag_semester_class_student_average_score_list_list,baseline_list,student_count_int,semester_list

# 计算班级三类人的成绩,得到三条线的成绩
def get_student_avg_score_group(tag_class_student_average_score_list,semester_list):
    # 初始化三类学生成绩表
    group_tag_class_student_average_score_list = [[],[],[]]
    # 初始化平均分基准线
    total_average_score_list = []
    # 根据学期长度遍历
    for semester_index_int in range(len(semester_list)):
        # 初始化三类学生成绩表
        top_avg_list = []
        med_avg_list = []
        low_avg_list = []

        for score_list in tag_class_student_average_score_list:
            # 根据分类标记添加到不同的列表中
            if score_list[0] == 1:
                top_avg_list.append(score_list[semester_index_int+2])
            if score_list[0] == 2:
                med_avg_list.append(score_list[semester_index_int+2])
            if score_list[0] == 3:
                low_avg_list.append(score_list[semester_index_int+2])

        # 得到平均分
        top_avg = public_function.get_average_from_list(top_avg_list)
        med_avg = public_function.get_average_from_list(med_avg_list)
        low_avg = public_function.get_average_from_list(low_avg_list)

        # 记录平均分
        group_tag_class_student_average_score_list[0].append(top_avg)
        group_tag_class_student_average_score_list[1].append(med_avg)
        group_tag_class_student_average_score_list[2].append(low_avg)

        # 记录平均分基准线
        average_total_score_list = [top_avg,med_avg,low_avg]
        # 获得总平均分
        total_average_score_float = public_function.get_average_from_list(average_total_score_list)
        # 记录平均分基准线
        total_average_score_list.append(total_average_score_float)

    # 返回数据
    return group_tag_class_student_average_score_list,total_average_score_list

# 线条设置
def create_traces(student_score_list,baseline_list,semester_list):
    # 轨迹列表
    traces = []
    # name_list = ['排名前1/3学生成绩平均值', '排名中间1/3学生成绩平均值', '排名后1/3学生成绩平均值']
    # x 轴值，与每组 y 的长度一致
    x_value = []
    # 减去分类标记和学号占2位的长度
    for i in range(len(semester_list)):
        x_value.append(i)
    # 颜色列表,按顺序绿色,蓝色,红色
    color_list = ['#008000', '#0070ff', '#ff033e']
    # 添加成绩线
    # 遍历 y_values 创建数据线
    for i, y in enumerate(student_score_list):
        # 根据第一个数据的值设置颜色
        if y[0] == 1:
            # color = 'green'  # 绿色
            color = color_list[0]  # 绿色
            # name = '入学成绩班级前30%'
            legendgroup = 'green_group'
            legendrank=1
        elif y[0] == 2:
            # color = 'blue'   # 蓝色
            color = color_list[1]   # 蓝色
            # name = '入学成绩班级中间40%'
            legendgroup = 'blue_group'
            legendrank=2
        else:
            # color = 'red'    # 红色
            color = color_list[2]    # 红色
            # name = '入学成绩班级后30%'
            legendgroup = 'red_group'
            legendrank=3

        # 创建数据点
        trace = plotly.graph_objs.Scatter(
            x=x_value,  # 使用固定长度的 x_values
            y=y[2:],  # y 数据,从索引2开始
            mode='lines+markers',
            # name=name,
            # 单独设置图例名称为列表索引1的元素
            name=student_score_list[i][1],
            # line=dict(color=color,dash='dash'),  # 设置线条颜色、线型
            line=dict(color=color,dash='solid'),  # 设置线条、线型
            # opacity=0.5,  # 设置透明度
            # 如果要分组显示,取消以下3行注释,给第4行加上注释
            # showlegend=show_legend[color],  # 控制图例显示
            # legendgroup=legendgroup,  # 同一组图例
            # legendrank=legendrank  # 设置图例顺序
            showlegend=True,  # 直接设置为True
        )
        traces.append(trace)

    # 设置基准线
    for i, baseline in enumerate(baseline_list):
        if i == 0:
            color='rgb(0,0,0)'
        if i == 1:
            color='rgb(246,193,77)'
        # 基准线
        standard_traces = plotly.graph_objs.Scatter(
            # x值列表
            x=x_value,
            # y值列表
            y=baseline[1:],
            mode='lines',
            # 名称
            name=baseline[0],
            line=dict(color=color, dash='dot'),
            showlegend=True
        )
        # 将标准线添加到 traces 列表中
        traces.append(standard_traces)

    return traces,x_value

# 坐标轴、图例等设置
def get_layout(traces,x_value,semester_list,college_name, class_name, course_type_name, student_count_int, class_teacher_name, width, height, y_axis_dtick):
    layout = plotly.graph_objs.Layout(
        title={
            'text': f"{college_name}_{class_name}_{course_type_name}_成绩走势图<br><sub>班级有成绩人数: {student_count_int}  班主任: {class_teacher_name}</sub>",
            'x': 0.5,
            'xanchor': 'center'
        },
        plot_bgcolor='white',paper_bgcolor='white',
        xaxis=dict(
            title='学期',showgrid=False,zeroline=True,showline=True,linecolor='black',
            rangemode='tozero',dtick=1,
            # 设置 x 轴范围为 x_value 的范围
            # range=[x_value[0], x_value[-1]],
            # 自动调整x轴范围
            autorange=True,
            # 设置 x 轴刻度文本
            tickvals=x_value,
            # ticktext=['入学成绩折算分数（百分制）', '第1学年', '第2学年', '第3学年', '第4学年']
            ticktext=semester_list
        ),
        yaxis=dict(
            title='平均成绩',showgrid=True,zeroline=True,showline=True, linecolor='black',gridcolor='lightgrey',
            # rangemode='tozero',
            # range=[y_axis_range[0], y_axis_range[1]],
            # 自动调整y轴范围
            autorange=True,
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

# 将数据以折线图方式呈现,单个班单个人
def show_score_line_chart(college_name_str,class_name_str,course_type_name,width,height,y_axis_dtick):

    # 获得班级成绩,多个学期,并添加标记
    tag_class_student_average_score_list,baseline_list,student_count_int,semester_list = get_score_by_semester(class_name_str,course_type_name)
    
    # 获得班级班主任姓名
    excute_sql_flag_str,excute_count_int,rows = database_score.get_class_teacher_by_class_name(class_name_str)
    # 如果没查询到数据
    if len(rows) == 0:
        class_teacher_name = None
    else:
        class_teacher_name=rows[0].班主任
    # 设置y轴范围
    # min_value, max_value = public_function.get_min_max_in_list(tag_class_student_average_score_list)
    
    # 基准线插入图例说明
    baseline_list[0][0:0]= ['班级前30%成绩基准线']
    baseline_list[1][0:0]= ['班级前70%成绩基准线']

    # 创建轨迹，用于展示分数分布
    traces,x_value = create_traces(tag_class_student_average_score_list,baseline_list,semester_list)
    # 创建布局，设置图表的标题、y轴标签、图例等
    layout_plotly = get_layout(traces,x_value,semester_list,college_name_str, class_name_str, course_type_name, student_count_int, class_teacher_name, width, height, y_axis_dtick)

    # 创建图表，并设置数据和布局
    fig_plotly = plotly.graph_objs.Figure(data=traces, layout=layout_plotly)

    # 将图表保存为图片
    # file_name = 'test.png'
    # plotly.io.write_image(fig_plotly, file_name)

    # print(f'成功保存{file_name}图片')

    return fig_plotly
    
# 将数据以折线图方式呈现,单个班三类人
def show_score_line_chart_group(college_name_str,class_name_str,course_type_name,width,height,y_axis_dtick):
    # 获得班级成绩,多个学期,并添加标记
    tag_class_student_average_score_list,baseline_list,student_count_int,semester_list = get_score_by_semester(class_name_str,course_type_name)
    
    # 获得三类人的成绩
    group_tag_class_student_average_score_list,total_average_score_list = get_student_avg_score_group(tag_class_student_average_score_list,semester_list)

    # 添加标记和占位符,使用修改列表切片的方式一次添加多个数据
    group_tag_class_student_average_score_list[0][0:0] = [1,'第一次成绩排名前30%学生成绩平均']
    group_tag_class_student_average_score_list[1][0:0] = [2,'第一次成绩排名中间40%学生成绩平均']
    group_tag_class_student_average_score_list[2][0:0] = [3,'第一次成绩排名后30%学生成绩平均']
    
    # 基准线插入图例说明
    total_average_score_list=[total_average_score_list]
    total_average_score_list[0][0:0]= [f'班级{course_type_name}成绩平均分']

    # 获得班级班主任姓名
    excute_sql_flag_str,excute_count_int,rows = database_score.get_class_teacher_by_class_name(class_name_str)
    # 如果没查询到数据
    if len(rows) == 0:
        class_teacher_name = None
    else:
        class_teacher_name=rows[0].班主任
    # 设置y轴范围
    # min_value, max_value = public_function.get_min_max_in_list(group_tag_class_student_average_score_list)
    
    # 创建轨迹，用于展示分数分布
    traces,x_value = create_traces(group_tag_class_student_average_score_list,total_average_score_list,semester_list)
    # 创建布局，设置图表的标题、y轴标签、图例等
    layout_plotly = get_layout(traces,x_value,semester_list,college_name_str, class_name_str, course_type_name, student_count_int, class_teacher_name, width, height, y_axis_dtick)

    # 创建图表，并设置数据和布局
    fig_plotly = plotly.graph_objs.Figure(data=traces, layout=layout_plotly)

    # 将图表保存为图片
    # file_name = 'test.png'
    # plotly.io.write_image(fig_plotly, file_name)

    # print(f'成功保存{file_name}图片')

    return fig_plotly

# 将数据以折线图方式呈现,多个图
def show_score_line_chart_group_all(college_name_str,class_name_str,course_type_name,width,height,y_axis_dtick):

    # 第1个图

    # 获得班级成绩,多个学期,并添加标记
    tag_class_student_average_score_list,baseline_list,student_count_int,semester_list = get_score_by_semester(class_name_str,course_type_name)
    
    # 获得班级班主任姓名
    excute_sql_flag_str,excute_count_int,rows = database_score.get_class_teacher_by_class_name(class_name_str)
    # 如果没查询到数据
    if len(rows) == 0:
        class_teacher_name = None
    else:
        class_teacher_name=rows[0].班主任
    # 设置y轴范围
    # min_value, max_value = public_function.get_min_max_in_list(tag_class_student_average_score_list)
    
    # 基准线插入图例说明
    baseline_list[0][0:0]= ['班级前30%成绩基准线']
    baseline_list[1][0:0]= ['班级前70%成绩基准线']

    # 创建轨迹，用于展示分数分布
    traces,x_value = create_traces(tag_class_student_average_score_list,baseline_list,semester_list)
    # 创建布局，设置图表的标题、y轴标签、图例等
    layout_plotly = get_layout(traces,x_value,semester_list,college_name_str, class_name_str, course_type_name, student_count_int, class_teacher_name, width, height, y_axis_dtick)

    # 创建图表，并设置数据和布局
    line_chart_fig_plotly = plotly.graph_objs.Figure(data=traces, layout=layout_plotly)

    # 第2个图
    # 获得三类人的成绩
    group_tag_class_student_average_score_list,total_average_score_list = get_student_avg_score_group(tag_class_student_average_score_list,semester_list)

    # 添加标记和占位符,使用修改列表切片的方式一次添加多个数据
    group_tag_class_student_average_score_list[0][0:0] = [1,'第一次成绩排名前30%学生成绩平均']
    group_tag_class_student_average_score_list[1][0:0] = [2,'第一次成绩排名中间40%学生成绩平均']
    group_tag_class_student_average_score_list[2][0:0] = [3,'第一次成绩排名后30%学生成绩平均']

    # 基准线插入图例说明
    total_average_score_list=[total_average_score_list]
    total_average_score_list[0][0:0]= [f'班级{course_type_name}成绩平均分']

    # 设置y轴范围
    # min_value, max_value = public_function.get_min_max_in_list(group_tag_class_student_average_score_list)
    
    # 创建轨迹，用于展示分数分布
    traces,x_value = create_traces(group_tag_class_student_average_score_list,total_average_score_list,semester_list)
    # 创建布局，设置图表的标题、y轴标签、图例等
    layout_plotly = get_layout(traces,x_value,semester_list,college_name_str, class_name_str, course_type_name, student_count_int, class_teacher_name, width, height, y_axis_dtick)

    # 创建图表，并设置数据和布局
    group_line_chart_fig_plotly = plotly.graph_objs.Figure(data=traces, layout=layout_plotly)

    return line_chart_fig_plotly,group_line_chart_fig_plotly

if __name__ == '__main__':
    # 引入文件目录设置
    import sys
    import os
    # 添加项目文件根目录到系统路径
    module_path = os.path.abspath('SCAU_JWC_2024_09_20')
    sys.path.append(module_path)

    # 引入模板文件
    from app.score_visualization.database import database_score
    from app import public_function


    # 查询测试
    college_name_str = '农学院'
    class_name_str = '农学202002'
    course_type_name = '必修'
    # 学期
    semester_list = ['2022-2023-1','2022-2023-2','2023-2024-1']
    
    # 获得班级成绩,单个学期
    # average_class_student_score_list,top_30_percent_score_float,top_70_percent_score_float = get_score_simple_semester(class_name_str,course_type_name,semester_list[0])

    # 获得班级成绩,多个学期,并添加标记
    # tag_class_student_average_score_list_list,top_30_percent_score_list,top_70_percent_score_list = get_score_by_semester(class_name_str,class_type_str,semester_list)
    
    # 图像布局设置
    width = 1000
    height = 600
    y_axis_dtick = 5

    # 将数据绘图为折线图
    fig_plotly = show_score_line_chart(college_name_str,class_name_str,course_type_name,width,height,y_axis_dtick)
    # fig_plotly = show_score_line_chart_group(college_name_str,class_name_str,course_type_name,width,height,y_axis_dtick)

    # excute_sql_flag_str,excute_count_int,rows = database_score.get_all_semester_by_class('林学202001')
    # # 初始化学期列表
    # semester_list = []
    # for row in rows:
    #     semester_list.append(row.学期)
    # # 获得班级成绩,多个学期,并添加标记
    # semester_list = sort_semester_list(semester_list)
    # print(semester_list)