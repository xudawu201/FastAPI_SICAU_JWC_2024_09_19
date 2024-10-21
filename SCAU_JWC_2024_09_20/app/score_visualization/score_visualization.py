'''
Author: xudawu
Date: 2024-10-21 15:35:21
LastEditors: xudawu
LastEditTime: 2024-10-21 18:02:35
'''

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
# from app.template import TemplatesJinja2ScoreVisualization

router = APIRouter()

import plotly.graph_objects as go
import plotly.io as pio

# 获得所有数据
def get_score(select_sql_str):
    # 执行sql语句,返回执行标志和执行数据
    excute_sql_flag_str,excute_count_int,rows = crud.select_table(select_sql_str)
    return excute_sql_flag_str,excute_count_int,rows

# 成绩可视化页
@router.get("/score_visualization", response_class=HTMLResponse)
async def score_visualization_page(request: Request):
    
    # 创建折线图数据
    fig = go.Figure()

    # 添加第一个系列
    fig.add_trace(go.Scatter(
        x=[1, 2, 3, 4, 5],
        y=[2, 3, 5, 4, 6],
        mode='lines+markers',
        name='系列1'
    ))

    # 添加第二个系列
    fig.add_trace(go.Scatter(
        x=[1, 2, 3, 4, 5],
        y=[1, 3, 4, 2, 5],
        mode='lines+markers',
        name='系列2'
    ))

    # 设置图表布局
    fig.update_layout(
        title='可交互的折线图示例',
        xaxis_title='X 轴',
        yaxis_title='Y 轴',
        # hovermode='x unified'
    )
    # 修改配置
    config_dict = {
        'displayModeBar': True,
        'doubleClick': 'reset',
        'scrollZoom':True,
        # 可修改标题
        'editable': True,
        'showLink': False,
        # 隐藏plotly的logo
        'displaylogo': False,
        'modeBarButtonsToAdd':['toggleSpikelines',]
        }
    # 将图表转换为HTML
    graph_html = pio.to_html(fig, full_html=False, include_plotlyjs='cdn', config=config_dict)

    # route_user = user.cookie_tokens_dict.get(session_token)
    context = {"request": request, "graph_html": graph_html}
    return TemplatesJinja2ScoreVisualization.TemplateResponse("score_visualization.html", context)

if __name__ == '__main__':
    # 引入文件目录设置
    import sys
    import os
    # 添加项目文件根目录到系统路径
    module_path = os.path.abspath('SCAU_JWC_2024_09_20')
    sys.path.append(module_path)

    # 引入模板文件
    from app.template import TemplatesJinja2ScoreVisualization

    from service import crud

    # 查询测试
    class_name_str = '金融202003'
    class_type_str = '必修'
    # 学期
    semester_str = '2022-2023-2'

    # 构造sql语句
    select_sql_str =f"select * from 成绩 where 班级 = '{class_name_str}' and 课程性质 = '{class_type_str}' and 学期 = '{semester_str}'"


    excute_sql_flag_str,excute_count_int,rows = get_score(select_sql_str)
    print(excute_sql_flag_str,excute_count_int)
    print(rows[0])
    print(rows[1])

    # 获得指定学生的成绩
    # for row in rows:
    #     if row.学号 == '202002998':
    #         print(row.课程,row.成绩)
