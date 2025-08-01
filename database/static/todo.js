async function loadData() {
    try {
      let response = await fetch(`/todo/tasks`);
      if (!response.ok) {
        console.error("Error fetching tasks:", response.statusText);
        return;
      }
      let tasks = await response.json();
      let todoList = document.getElementById("todoList");
      todoList.innerHTML = "";

      tasks.forEach((task) => {
        let li = document.createElement("li");
        li.classList.toggle("completed", task.is_completed);

        let checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.checked = task.is_completed;
        checkbox.onclick = () =>
          toggleTaskCompletion(task.task_id, task.is_completed);
        checkbox.classList.add("task-checkbox");

        let taskText = document.createElement("span");
        taskText.innerText = `${task.task} (Priority: ${
          task.priority
        }, Due: ${task.due_date || "No due date"})`;
        taskText.classList.add("task-text");

        let deleteBtn = document.createElement("button");
        deleteBtn.innerHTML = "🗑️";
        deleteBtn.onclick = () => deleteTask(task.task_id);
        deleteBtn.classList.add("delete-btn");

        li.appendChild(checkbox);
        li.appendChild(taskText);
        li.appendChild(deleteBtn);
        todoList.appendChild(li);
      });
    } catch (error) {
      console.error("Error in loadData:", error);
    }
  }
  async function addTask() {
    const taskText = document.getElementById("newTask").value;
    const priority = document.getElementById("taskPriority").value;
    const dueDate = document.getElementById("taskDueDate").value || null;

    if (!taskText) {
      alert("Task cannot be empty!");
      return;
    }

    try {
      let response = await fetch("/todo", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          task: taskText,
          priority: priority,
          due_date: dueDate,
        }),
      });
      if (!response.ok) {
        console.error("Error adding task:", response.statusText);
      } else {
        document.getElementById("newTask").value = "";
        loadData();
      }
    } catch (error) {
      console.error("Error in addTask:", error);
    }
  }

  // Function to toggle task completion status
  async function toggleTaskCompletion(taskId, isCompleted) {
    try {
      await fetch(`/todo/complete/${taskId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ is_completed: !isCompleted }),
      });
      loadData();
    } catch (error) {
      console.error("Error in toggleTaskCompletion:", error);
    }
  }

  // Function to delete a task
  async function deleteTask(taskId) {
    try {
      await fetch(`/todo/${taskId}`, { method: "DELETE" });
      loadData();
    } catch (error) {
      console.error("Error in deleteTask:", error);
    }
  }
