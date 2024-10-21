'''
Author: xudawu
Date: 2024-10-15 15:11:37
LastEditors: xudawu
LastEditTime: 2024-10-21 11:02:30
'''
from fastapi.templating import Jinja2Templates

# 定义模板目录

# 公共页面模板
TemplatesJinja2Public = Jinja2Templates(directory="SCAU_JWC_2024_09_20\\frontend\\template")
# 登录注册页模板
TemplatesJinja2Login = Jinja2Templates(directory="SCAU_JWC_2024_09_20\\app\\login\\frontend\\template")
# 成绩可视化模板
TemplatesJinja2ScoreVisualization = Jinja2Templates(directory="SCAU_JWC_2024_09_20\\app\\score_visualization\\frontend\\template")