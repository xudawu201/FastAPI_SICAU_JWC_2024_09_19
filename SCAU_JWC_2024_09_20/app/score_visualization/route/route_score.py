'''
Author: xudawu
Date: 2024-10-24 14:45:08
LastEditors: xudawu
LastEditTime: 2024-10-24 17:51:14
'''
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
import plotly
import copy
import math

# 引入自定义文件
from app.template import TemplatesJinja2ScoreVisualization
from app.score_visualization.service import service_score_visualization
from app.score_visualization.service import service_filter_score_info


router = APIRouter()

# 成绩可视化页
@router.get("/score_visualization", response_class=HTMLResponse)
async def score_visualization_page(request: Request):
    
    # 班级名称
    class_name_str = '农学202001'
    # 课程类型
    course_type_name = '必修'
    # 学期
    semester_list = ['2020-2021-1','2020-2021-2','2021-2022-1','2021-2022-2','2022-2023-1','2022-2023-2','2023-2024-1','2023-2024-2']
    
    # 图像布局设置
    width = 1000
    height = 600
    y_axis_dtick = 5

    # 将数据绘图为折线图
    fig_plotly = service_score_visualization.show_score_line_chart(class_name_str,course_type_name,semester_list,width,height,y_axis_dtick)

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
    graph_html = plotly.io.to_html(fig_plotly, full_html=False, include_plotlyjs='cdn', config=config_dict)

    # route_user = user.cookie_tokens_dict.get(session_token)

    # 获取筛选框数据
    # rows = service_filter_score_info.get_all_score_info()

    context = {"request": request, "graph_html": graph_html}
    return TemplatesJinja2ScoreVisualization.TemplateResponse("score_visualization.html", context)

# 获取筛选框数据
@router.post("/filter_score")
async def filter_score(request: Request):
    # 获取请求体中的 JSON 数据
    request_data = await request.json()
    password_str = request_data.get("password")
    print(password_str)
    # 示例数据
    college_dict = {
        "computer": ["计算机1班", "计算机2班", "计算机3班"],
        "business": ["商科1班", "商科2班", "商科3班"]
    }
    # 初始化回应字典
    response_context_dict = {
            "username": '',
            'already_name_flag': '',
            "test": 'aaa',
            }

    # response_context_dict = {"request": request,"college_dict":college_dict}

    return response_context_dict
