'''
Author: xudawu
Date: 2024-10-24 14:45:08
LastEditors: xudawu
LastEditTime: 2024-10-29 16:30:03
'''
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
import fastapi
import plotly

# 引入自定义文件
from app.template import TemplatesJinja2ScoreVisualization
from app.score_visualization.service import service_score_visualization
from app.score_visualization.service import service_filter_score_info


router = APIRouter()

# 配置超参数信息

# 图像布局设置
width = 1100
height = 600
y_axis_dtick = 5

# 修改配置
config_dict = {
    'displayModeBar': True,
    'doubleClick': 'reset',
    'scrollZoom':True,
    # 可修改标题
    'editable': True,
    # 隐藏plotly的链接
    'showLink': False,
    # 隐藏plotly的logo
    'displaylogo': False,
    # 增加按钮
    'modeBarButtonsToAdd':['toggleSpikelines',],
    # 移除按钮
    'modeBarButtonsToRemove': ['select2d','lasso2d'],
    }

# 成绩可视化页
@router.get("/score_visualization", response_class=HTMLResponse)
async def score_visualization_page(request: Request,college_name_str='农学院',class_name_str='农学202001',course_type_name_str = '必修'):
    
    # 将数据绘图为折线图
    line_chart_fig_plotly,group_line_chart_fig_plotly = service_score_visualization.show_score_line_chart_group_all(college_name_str,class_name_str,course_type_name_str,width,height,y_axis_dtick)
    
    # 将班级每个人成绩图表转换为HTML
    line_chart_html = plotly.io.to_html(line_chart_fig_plotly, full_html=False, include_plotlyjs='cdn', config=config_dict)

    # 将班级分组成绩图表转换为HTML
    group_line_chart_html = plotly.io.to_html(group_line_chart_fig_plotly, full_html=False, include_plotlyjs='cdn', config=config_dict)

    context = {"request": request, "line_chart_html": line_chart_html,'group_line_chart_html':group_line_chart_html}
    return TemplatesJinja2ScoreVisualization.TemplateResponse("score_visualization.html", context)

# 获取筛选框数据
@router.post("/filter_score")
async def filter_score(request: Request):
    # 示例数据
    # college_dict = {
    #     "计算机学院": ["计算机1班", "计算机2班", "计算机3班"],
    #     "business": ["商科1班", "商科2班", "商科3班"]
    # }

    # 获取所有学院和班级
    college_class_dict = service_filter_score_info.get_all_college_class_dict()

    # 返回响应
    return college_class_dict

# 获取提交的班级信息
@router.post("/submit_class_name")
# 获取提交的筛选信息
async def submit_class_name(request: Request):
    # 获取请求体中的 JSON 数据
    request_data = await request.json()
    college_str = request_data.get("college_str")
    class_name_str = request_data.get("class_str")

    # 初始化回应字典
    response_context_dict = {
            'message':['aaa']
            }
    response_context_dict['course_type_list'] = service_filter_score_info.get_all_have_score_course_type_by_class(class_name_str)
    
    return response_context_dict

# 获取提交的筛选信息
@router.post("/submit_select_info")
async def submit_select_info(request: Request):
    # 获取请求体中的 JSON 数据
    request_data = await request.json()
    college_name_str = request_data.get("college_name_str")
    class_name_str = request_data.get("class_name_str")
    course_type_name_str = request_data.get("course_type_name_str")

    # 将数据绘图为折线图
    line_chart_fig_plotly,group_line_chart_fig_plotly = service_score_visualization.show_score_line_chart_group_all(college_name_str,class_name_str,course_type_name_str,width,height,y_axis_dtick)
    
    # 将班级每个人成绩图表转换为HTML
    line_chart_html = plotly.io.to_html(line_chart_fig_plotly, full_html=False, include_plotlyjs='cdn', config=config_dict)

    # 将班级分组成绩图表转换为HTML
    group_line_chart_html = plotly.io.to_html(group_line_chart_fig_plotly, full_html=False, include_plotlyjs='cdn', config=config_dict)
    
    # 返回图标html
    return fastapi.responses.JSONResponse(
        content={
            "line_chart_html": line_chart_html,
            "group_line_chart_html": group_line_chart_html,
            }
            )

