from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    # 默认值
    default_value = "Hello, World!"
    return templates.TemplateResponse("TempTest_02_2024_10_14.html", {"request": request, "data": default_value})

@app.post("/", response_class=HTMLResponse)
async def submit_form(request: Request, name: str = Form(...)):
    # 更新数据
    updated_value = f"Hello, {name}!"
    return templates.TemplateResponse("TempTest_02_2024_10_14.html", {"request": request, "data": updated_value})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)