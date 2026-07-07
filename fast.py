from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import json
import os

app = FastAPI(title="Student Management System")

FILE_NAME = "students.txt"

# ----------------------------
# Default Student Data
# ----------------------------
default_students = {
    1: {"name": "Benhur", "age": 20, "course": "B.Tech", "sem": 4, "marks": 82},
    2: {"name": "Denson", "age": 21, "course": "B.Tech", "sem": 6, "marks": 88},
    3: {"name": "Vivek", "age": 21, "course": "B.Tech", "sem": 6, "marks": 91},
    4: {"name": "Vedic", "age": 20, "course": "B.Tech", "sem": 6, "marks": 79},
    5: {"name": "Vedant", "age": 22, "course": "B.Tech", "sem": 6, "marks": 95},
    6: {"name": "Deepa", "age": 21, "course": "B.Tech", "sem": 6, "marks": 86},
    7: {"name": "Sunibala", "age": 21, "course": "B.Tech", "sem": 6, "marks": 90},
    8: {"name": "Jesmita", "age": 20, "course": "B.Tech", "sem": 6, "marks": 84},
}


def load_data():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            data = json.load(file)
            return {int(k): v for k, v in data.items()}
    return default_students.copy()


students = load_data()


def save_data():
    with open(FILE_NAME, "w") as file:
        json.dump(students, file, indent=4)


def grade(marks):
    if marks >= 90:
        return "A+"
    elif marks >= 80:
        return "A"
    elif marks >= 70:
        return "B"
    elif marks >= 60:
        return "C"
    elif marks >= 50:
        return "D"
    return "F"


@app.get("/", response_class=HTMLResponse)
def home():

    html = """
    <!DOCTYPE html>
    <html>
    <head>
    <title>Student Management</title>

    <style>

    body{
        font-family:Arial;
        background:#f2f2f2;
        text-align:center;
    }

    h1{
        color:#333;
    }

    table{
        width:90%;
        margin:auto;
        border-collapse:collapse;
        background:white;
    }

    th{
        background:#4CAF50;
        color:white;
        padding:10px;
    }

    td{
        padding:10px;
        border:1px solid #ccc;
    }

    tr:nth-child(even){
        background:#f9f9f9;
    }

    </style>
    </head>

    <body>

    <h1>Student Management System</h1>

    <table>

    <tr>
    <th>ID</th>
    <th>Name</th>
    <th>Age</th>
    <th>Course</th>
    <th>Semester</th>
    <th>Marks</th>
    <th>Grade</th>
    </tr>
    """

    for sid, s in students.items():
        html += f"""
        <tr>
            <td>{sid}</td>
            <td>{s['name']}</td>
            <td>{s['age']}</td>
            <td>{s['course']}</td>
            <td>{s['sem']}</td>
            <td>{s['marks']}</td>
            <td>{grade(s['marks'])}</td>
        </tr>
        """

    html += """
    </table>
    </body>
    </html>
    """

    return HTMLResponse(content=html)


@app.get("/students")
def display_students():
    return students
@app.get("/student/{sid}")
def get_student(sid: int):
    if sid in students:
        return {"id": sid, "student": students[sid]}
    return {"message": "Student not found"}


@app.get("/search/{name}")
def search_student(name: str):
    result = {}

    for sid, data in students.items():
        if data["name"].lower() == name.lower():
            result[sid] = data

    if result:
        return result

    return {"message": "Student not found"}


@app.post("/add_student")
def add_student(
    sid: int,
    name: str,
    age: int,
    course: str,
    sem: int,
    marks: float,
):
    if sid in students:
        return {"message": "Student ID already exists"}

    students[sid] = {
        "name": name,
        "age": age,
        "course": course,
        "sem": sem,
        "marks": marks,
    }

    save_data()

    return {
        "message": "Student added successfully",
        "student": students[sid],
    }


@app.put("/update_student/{sid}")
def update_student(
    sid: int,
    name: str,
    age: int,
    course: str,
    sem: int,
    marks: float,
):
    if sid not in students:
        return {"message": "Student not found"}

    students[sid] = {
        "name": name,
        "age": age,
        "course": course,
        "sem": sem,
        "marks": marks,
    }

    save_data()

    return {
        "message": "Student updated successfully",
        "student": students[sid],
    }


@app.delete("/delete_student/{sid}")
def delete_student(sid: int):
    if sid not in students:
        return {"message": "Student not found"}

    deleted = students.pop(sid)

    save_data()

    return {
        "message": "Student deleted successfully",
        "student": deleted,
    }


@app.get("/average")
def average_marks():
    if len(students) == 0:
        return {"average_marks": 0}

    total = sum(student["marks"] for student in students.values())

    return {
        "average_marks": round(total / len(students), 2)
    }


@app.get("/topper")
def topper():
    if len(students) == 0:
        return {"message": "No students available"}

    top_id = max(
        students,
        key=lambda x: students[x]["marks"]
    )

    return {
        "id": top_id,
        "student": students[top_id],
        "grade": grade(students[top_id]["marks"]),
    }


@app.get("/save")
def save_students():
    save_data()
    return {
        "message": "Students saved successfully to students.txt"
    }


@app.get("/stats")
def statistics():
    if not students:
        return {"message": "No students available"}

    marks = [s["marks"] for s in students.values()]

    return {
        "total_students": len(students),
        "highest_marks": max(marks),
        "lowest_marks": min(marks),
        "average_marks": round(sum(marks) / len(marks), 2),
    }


@app.get("/grades")
def all_grades():
    result = {}

    for sid, student in students.items():
        result[sid] = {
            "name": student["name"],
            "marks": student["marks"],
            "grade": grade(student["marks"]),
        }

    return result


@app.get("/pass")
def pass_students():
    passed = {}

    for sid, student in students.items():
        if student["marks"] >= 50:
            passed[sid] = student

    return passed


@app.get("/fail")
def fail_students():
    failed = {}

    for sid, student in students.items():
        if student["marks"] < 50:
            failed[sid] = student

    return failed
