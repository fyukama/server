from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request

app = FastAPI(title="Todo API")

todos = [
    "Eat Food",
    "Wash Clothes"
]

not_to_do_list = []

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    )


@app.get("/todos")
def show_all_todos():
    return {
        "todos": todos
    }


@app.get("/todo/{task}")
def get_todo(task: str):
    if task in todos:
        return {
            "message": "Task Found",
            "task": task
        }

    return {
        "message": "Task Not Found"
    }


@app.post("/todo")
def add_todo(task: str):

    todos.append(task)

    return {
        "message": "Todo Added Successfully",
        "data": todos
    }


@app.post("/nottodo")
def add_not_todo(task: str):

    not_to_do_list.append(task)

    return {
        "message": "Added to Not-To-Do List",
        "data": not_to_do_list
    }


@app.delete("/delete_todo")
def delete_todo(task: str):

    if task in todos:
        todos.remove(task)

        return {
            "message": "Task Deleted Successfully",
            "data": todos
        }

    return {
        "message": "Task Not Found"
    }


@app.put("/edit_todo")
def edit_todo(old_task: str, new_task: str):

    if old_task in todos:

        index = todos.index(old_task)

        todos[index] = new_task

        return {
            "message": "Task Updated Successfully",
            "data": todos
        }

    return {
        "message": "Task Not Found"
    }


@app.get("/nottodos")
def show_not_todos():

    return {
        "Not_To_Do_List": not_to_do_list
    }
