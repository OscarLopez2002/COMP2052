// Agregar nueva tarea
document
  .getElementById("addTaskForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    const todo = document.getElementById("todo").value;
    const data = { todo: todo };

    fetch("/todos", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Success:", data);
        // Agregar la nueva tarea a la lista sin recargar la página
        const ul = document.querySelector(".task-list");
        const li = document.createElement("li");
        li.classList.add("task-item");
        li.id = `${todo}`;
        li.innerHTML = `<span>${todo}</span>
        <div class="task-actions">
          <button class="btn btn-edit" onclick="editTask('${todo}')">Edit</button>
          <button class="btn btn-delete" onclick="deleteTask('${todo}')">Delete</button>
        </div>`;
        ul.appendChild(li);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  });

// Eliminar tarea
function deleteTask(todo) {
  fetch("/todos", {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ todo: todo }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Success:", data);
      // Eliminar el todo de la lista sin recargar la página
      document.getElementById(`${todo}`).remove();
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

// Editar tarea
function editTask(todo) {
  const newTodo = prompt("Enter the new task:", todo);
  if (newTodo && newTodo !== todo) {
    fetch("/todos", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ old: todo, new: newTodo }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Success:", data);
        // Actualizar el texto del todo sin recargar la página
        const taskItem = document.getElementById(`${todo}`);
        taskItem.querySelector("span").textContent = newTodo;
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }
}
