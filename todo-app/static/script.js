// Load all todos
async function loadTodos() {

    let response = await fetch("/todos");
    let data = await response.json();

    let list = document.getElementById("todoList");
    list.innerHTML = "";

    data.todos.forEach(task => {

        let li = document.createElement("li");

        li.innerHTML = `
            <span>${task}</span>

            <div>
                <button class="edit" onclick="editTodo('${task}')">
                    ✏️ Edit
                </button>

                <button class="delete" onclick="deleteTodo('${task}')">
                    🗑 Delete
                </button>
            </div>
        `;

        list.appendChild(li);

    });

}

// Add Todo
async function addTodo() {

    let task = document.getElementById("task").value.trim();

    if (task === "") {
        alert("Please enter a task.");
        return;
    }

    await fetch("/todo?task=" + encodeURIComponent(task), {
        method: "POST"
    });

    document.getElementById("task").value = "";

    loadTodos();

}

// Delete Todo
async function deleteTodo(task) {

    let confirmDelete = confirm("Delete this task?");

    if (!confirmDelete) return;

    await fetch("/delete_todo?task=" + encodeURIComponent(task), {
        method: "DELETE"
    });

    loadTodos();

}

// Edit Todo
async function editTodo(oldTask) {

    let newTask = prompt("Edit your task:", oldTask);

    if (newTask === null) return;

    newTask = newTask.trim();

    if (newTask === "") {
        alert("Task cannot be empty.");
        return;
    }

    await fetch(
        "/edit_todo?old_task=" +
        encodeURIComponent(oldTask) +
        "&new_task=" +
        encodeURIComponent(newTask),
        {
            method: "PUT"
        }
    );

    loadTodos();

}

// Search Todo
async function searchTodo() {

    let keyword = document
        .getElementById("task")
        .value
        .toLowerCase();

    let response = await fetch("/todos");
    let data = await response.json();

    let list = document.getElementById("todoList");
    list.innerHTML = "";

    data.todos.forEach(task => {

        if (task.toLowerCase().includes(keyword)) {

            let li = document.createElement("li");

            li.innerHTML = `
                <span>${task}</span>

                <div>
                    <button class="edit" onclick="editTodo('${task}')">
                        ✏️ Edit
                    </button>

                    <button class="delete" onclick="deleteTodo('${task}')">
                        🗑 Delete
                    </button>
                </div>
            `;

            list.appendChild(li);

        }

    });

}

// Load todos when page opens
window.onload = loadTodos;
