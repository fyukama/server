from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

students = {
    1: {"name": "Ben", "sem": 4},
    2: {"name": "Deepa", "sem": 6},
    3: {"name": "Denson", "sem": 2},
    4: {"name": "Vivek", "sem": 5},
    5: {"name": "Vedant", "sem": 3},
    6: {"name": "Vedic", "sem": 1},
    7: {"name": "Jeshmita", "sem": 7},
    8: {"name": "Sunibala", "sem": 8},
    9: {"name": "Duroi", "sem": 4},
    10: {"name": "Lemba", "sem": 6}
}

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
            table{
                margin:auto;
                border-collapse:collapse;
                width:60%;
                background:white;
            }
            th,td{
                border:1px solid black;
                padding:10px;
            }
            th{
                background:#4CAF50;
                color:white;
            }
            h1{
                color:#333;
            }
        </style>
    </head>
    <body>
        <h1>Student Management System</h1>

        <table>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Semester</th>
            </tr>
    """

    for sid, student in students.items():
        html += f"""
        <tr>
            <td>{sid}</td>
            <td>{student['name']}</td>
            <td>{student['sem']}</td>
        </tr>
        """

    html += """
        </table>
    </body>
    </html>
    """

    return html


@app.get("/student")
def get_students():
    return {"student_list": students}


@app.get("/student/{id}")
def get_student(id: int):
    if id in students:
        return students[id]
    return {"message": "Student not found"}
