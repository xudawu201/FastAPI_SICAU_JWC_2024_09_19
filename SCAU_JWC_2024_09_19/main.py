from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# 定义学生模型
class Student(BaseModel):
    id: int
    name: str
    age: int
    major: str

# 定义课程模型
class Course(BaseModel):
    id: int
    title: str
    description: str

# 模拟数据库
students_db: List[Student] = []
courses_db: List[Course] = []

# 获取所有学生
@app.get("/students", response_model=List[Student])
def get_students():
    return students_db

# 添加新学生
@app.post("/students", response_model=Student)
def add_student(student: Student):
    students_db.append(student)
    return student

# 获取所有课程
@app.get("/courses", response_model=List[Course])
def get_courses():
    return courses_db

# 添加新课程
@app.post("/courses", response_model=Course)
def add_course(course: Course):
    courses_db.append(course)
    return course

# 根据学生ID获取学生详情
@app.get("/students/{student_id}", response_model=Student)
def get_student(student_id: int):
    for student in students_db:
        if student.id == student_id:
            return student
    raise HTTPException(status_code=404, detail="Student not found")

# 根据课程ID获取课程详情
@app.get("/courses/{course_id}", response_model=Course)
def get_course(course_id: int):
    for course in courses_db:
        if course.id == course_id:
            return course
    raise HTTPException(status_code=404, detail="Course not found")

# 更新学生信息
@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, updated_student: Student):
    for index, student in enumerate(students_db):
        if student.id == student_id:
            students_db[index] = updated_student
            return updated_student
    raise HTTPException(status_code=404, detail="Student not found")

# 删除学生
@app.delete("/students/{student_id}", response_model=dict)
def delete_student(student_id: int):
    for index, student in enumerate(students_db):
        if student.id == student_id:
            del students_db[index]
            return {"detail": "Student deleted"}
    raise HTTPException(status_code=404, detail="Student not found")
