'''
Author: xudawu
Date: 2024-10-15 08:52:34
LastEditors: xudawu
LastEditTime: 2024-11-22 16:34:59
'''
# 引入文件目录设置
# import sys
# import os
# # 添加项目文件根目录到系统路径
# module_path = os.path.abspath('SCAU_JWC_2024_09_20')
# sys.path.append(module_path)

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from route import route_authorization, route_main
import uvicorn

# 引入业务路由模块
from app.score_visualization.route import route_score
from app.super_search.route import route_super_search
from app.course_schedule.route import route_course_schedule


# 创建 FastAPI 应用
# app = FastAPI()
# 部署项目时关闭api文档
app = FastAPI(openapi_url=None)

# 获得文件夹路径
BASE_PATH = Path(__file__).resolve().parent

# 挂载静态文件路径,公共静态文件路径
app.mount("/public_static_path", StaticFiles(directory= "frontend/static"))

# 业务模块静态文件路径
app.mount("/login_static_path", StaticFiles(directory="app/login/frontend/static"))
app.mount("/score_visualization_static_path", StaticFiles(directory="app/score_visualization/frontend/static"))
app.mount("/super_search_static_path", StaticFiles(directory="app/super_search/frontend/static"))
app.mount("/course_schedule_static_path", StaticFiles(directory="app/course_schedule/frontend/static"))


# 包含路由模块
app.include_router(route_authorization.router)
app.include_router(route_main.router)

# 成绩可视化模块
app.include_router(route_score.router)
# 超级查询模块
app.include_router(route_super_search.router)
# 排课系统模块
app.include_router(route_course_schedule.router)

# 主函数启动应用程序
if __name__ == "__main__":
    # 绑定到所有可用的网络接口,可以被任何 IP 地址访问
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
    # 仅绑定到本地回环接口,只能被本地计算机访问
    # uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
    # 绑定到特定的 IP 地址,为本机的固定ip,可以被局域网内其他能访问到此IP地址的计算机访问
    # uvicorn.run(app="main:app", host="10.128.42.18", port=8000, reload=True)