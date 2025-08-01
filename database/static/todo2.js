
document.addEventListener("DOMContentLoaded", async function () {
  console.log("Script loaded successfully!");

 
  let allTasks = [];
  let currentTag = "";


  async function fetchUserData() {
    const response = await fetch("/user-info"); // Create a new Flask route to return user details
    if (response.ok) {
      const data = await response.json();
      document.getElementById("userFullName").innerText = data.fullname;
      document.getElementById("userPoints").innerText = data.points;
    } else {
      console.error("Failed to fetch user data");
    }
  }

  fetchUserData();

  // ✅ Fetch tasks from backend
  async function fetchTasks() {
    const response = await fetch("/todo/tasks");
    if (response.ok) {
      allTasks = await response.json();
      console.log("Fetched tasks:", allTasks); // ✅ Debug: Check if tasks are fetched
      extractTags(); // ✅ Refresh tags sidebar
    } else {
      console.error("Failed to fetch tasks");
    }
  }

  await fetchTasks(); // Fetch tasks on page load

  // ✅ Always active dropdown listener
  const dropdownHeader = document.getElementById("tag-dropdown-header");
  dropdownHeader.addEventListener("click", function () {
    const tagContainer = document.getElementById("custom-category-list");
    tagContainer.classList.toggle("dropdown-visible");

    this.innerHTML = tagContainer.classList.contains("dropdown-visible")
      ? "Tags ▲"
      : "Tags ▼";
  });

  // ✅ Extract tags from tasks and update sidebar
  function extractTags() {
    const tags = new Set(); // Store unique tags
    allTasks.forEach((task) => {
      if (task.tag && task.tag.trim() !== "") {
        tags.add(task.tag);
      }
    });

    const tagContainer = document.getElementById("custom-category-list");
    tagContainer.innerHTML = ""; // Clear previous tags

    if (tags.size === 0) {
      tagContainer.innerHTML =
        "<p style='padding: 10px;'>No tags available.</p>";
      return;
    }

    // Add tags dynamically
    tags.forEach((tag) => {
      const tagElem = document.createElement("div");
      tagElem.className = "category";
      tagElem.setAttribute("data-tag", tag);
      tagElem.innerText = `#${tag}`;
      tagElem.addEventListener("click", () => loadTasksForTag(tag)); // Click to filter tasks
      tagContainer.appendChild(tagElem);
    });

    console.log("Updated tags:", Array.from(tags)); // Debugging log
  }

  // Dropdown toggle

  // ✅ Render task list dynamically
  function renderTasks(tasks, title) {
    const content = document.getElementById("content");
    let html = `<h1>${title}</h1><ul id="task-list">`;

    if (tasks.length === 0) {
      html += `<li>No tasks yet.</li>`;
    } else {
      tasks.forEach((task) => {
        let points = 0;
        if (task.priority === "Low") points = 5;
        if (task.priority === "Medium") points = 10;
        if (task.priority === "High") points = 20;

        html += `
            <li data-id="${task.task_id}" class="${
          task.is_completed ? "task-completed" : ""
        }">
                <input type="checkbox" class="task-checkbox" ${
                  task.is_completed ? "checked" : ""
                }>
                <span class="delete-bullet">🗑️</span>
                <span class="edit-bullet">✏️</span>
                <div class="task-details">
                    <div class="task-text" title="${
                      task.tag ? `#${task.tag}` : ""
                    }">
                        ${
                          task.task
                        } <span class="task-points">(${points} pts)</span>
                    </div>
                    <div class="task-date">${
                      task.due_date || "No due date"
                    }</div>
                </div>
            </li>`;
      });
    }

    html += `</ul><button id="new-task-button">New Task</button>`;
    content.innerHTML = html;

    attachTaskDeletionHandlers();
    attachTaskCompletionHandlers();
    attachNewTaskButtonHandler();
    attachTaskEditHandlers();
  }

  // ✅ Load tasks for specific tag
  function loadTasksForTag(tag) {
    currentTag = tag;
    const taggedTasks = allTasks.filter((task) => task.tag === tag);
    renderTasks(taggedTasks, `#${tag}`);
  }

  // ✅ Load today's tasks
  function loadTodayTasks() {
    currentTag = "";
    const today = new Date().toISOString().split("T")[0];
    const todayTasks = allTasks.filter((task) => task.due_date === today);
    renderTasks(todayTasks, "Today");
  }

  // ✅ Load upcoming tasks
  function loadUpcomingTasks() {
    currentTag = "";
    const today = new Date().toISOString().split("T")[0];
    const upcomingTasks = allTasks.filter((task) => task.due_date > today);
    renderTasks(upcomingTasks, "Upcoming");
  }
  // ✅ Task deletion handler
  function attachTaskDeletionHandlers() {
    document.querySelectorAll(".delete-bullet").forEach((bullet) => {
      bullet.addEventListener("click", async function () {
        const taskId = this.parentElement.getAttribute("data-id");
        const response = await fetch(`/todo/${taskId}`, { method: "DELETE" });
        if (response.ok) {
          console.log("Task deleted");
          await fetchTasks(); // Refresh data
          if (currentTag) loadTasksForTag(currentTag);
          else loadTodayTasks();
        } else {
          console.error("Failed to delete task");
        }
      });
    });
  }

  // ✅ Task completion handler
  function attachTaskCompletionHandlers() {
    document.querySelectorAll(".task-checkbox").forEach((checkbox) => {
      checkbox.addEventListener("change", async function () {
        const taskId = this.closest("li").getAttribute("data-id");
        const isCompleted = this.checked;

        const response = await fetch(`/todo/complete/${taskId}`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ is_completed: isCompleted }),
        });

        if (response.ok) {
          console.log("Task completion updated");

          // ✅ Fetch updated points from backend
          const data = await response.json();
          document.getElementById("userPoints").innerText = data.user_points;

          await fetchTasks(); // Refresh data
        } else {
          console.error("Failed to update completion");
        }
      });
    });
  }
  function attachTaskEditHandlers() {
    document.querySelectorAll(".edit-bullet").forEach((button) => {
      button.addEventListener("click", function () {
        const li = this.closest("li");
        const taskId = li.getAttribute("data-id");
        const taskText = li.querySelector(".task-text").innerText;
        const dueDate = li.querySelector(".task-date").innerText;
        const tag = li
          .querySelector(".task-text")
          .getAttribute("title")
          .replace("#", "");

        // 🎨 Build a popup form dynamically
        const editForm = document.createElement("div");
        editForm.innerHTML = `
        <div class="edit-task-form">
          <input type="text" id="edit-task-text" value="${taskText.trim()}" placeholder="Task title">
          <input type="text" id="edit-task-tag" value="${tag}" placeholder="Tag (without #)">
          <input type="date" id="edit-task-date" value="${
            dueDate !== "No due date" ? dueDate : ""
          }">
          <select id="edit-task-priority">
            <option value="Low">Low</option>
            <option value="Medium">Medium</option>
            <option value="High">High</option>
          </select>
          <button id="confirm-edit-task">Save</button>
          <button id="cancel-edit-task">Cancel</button>
        </div>
      `;
        li.appendChild(editForm); // Add inline edit form

        // ✅ Save Button Logic
        editForm
          .querySelector("#confirm-edit-task")
          .addEventListener("click", async function () {
            const updatedTask = editForm
              .querySelector("#edit-task-text")
              .value.trim();
            const updatedTag = editForm
              .querySelector("#edit-task-tag")
              .value.trim();
            const updatedDate = editForm.querySelector("#edit-task-date").value;
            const updatedPriority = editForm.querySelector(
              "#edit-task-priority"
            ).value;

            const response = await fetch(`/todo/${taskId}`, {
              method: "PUT",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                task: updatedTask,
                tag: updatedTag,
                due_date: updatedDate,
                priority: updatedPriority,
              }),
            });

            if (response.ok) {
              console.log("Task updated!");
              await fetchTasks(); // Refresh everything
              if (currentTag) loadTasksForTag(currentTag);
              else loadTodayTasks();
            } else {
              console.error("Failed to update task");
            }
          });

        // ❌ Cancel Button Logic
        editForm
          .querySelector("#cancel-edit-task")
          .addEventListener("click", function () {
            editForm.remove(); // Close form
          });
      });
    });
  }

  // ✅ New task creation handler
  function attachNewTaskButtonHandler() {
    document
      .getElementById("new-task-button")
      .addEventListener("click", function () {
        const content = document.getElementById("content");
        this.style.display = "none";

        const formHTML = `
        <div id="new-task-form">
          <input type="text" id="new-task-text" placeholder="Task (use #tag)">
          <input type="date" id="new-task-date" value="${
            new Date().toISOString().split("T")[0]
          }">
          <select id="new-task-priority">
            <option value="Low">Low</option>
            <option value="Medium" selected>Medium</option>
            <option value="High">High</option>
          </select>
          <button id="confirm-add-task-button">Add Task</button>
          <button id="cancel-add-task-button">Cancel</button>
        </div>`;
        this.insertAdjacentHTML("afterend", formHTML);

        // ✅ Handle form submission
        document
          .getElementById("confirm-add-task-button")
          .addEventListener("click", async function () {
            const fullInput = document
              .getElementById("new-task-text")
              .value.trim();
            const dueDate = document.getElementById("new-task-date").value;
            const priority = document.getElementById("new-task-priority").value;

            if (!fullInput) return alert("Task cannot be empty!");

            // ✅ Extract tag (without '#') and task title
            let tag = null;
            let taskTitle = fullInput;

            if (fullInput.includes("#")) {
              [taskTitle, tag] = fullInput.split("#").map((s) => s.trim());
            }

            // 🔍 Debugging Output
            console.log("📩 Full Input:", fullInput);
            console.log("📌 Extracted Task Title:", taskTitle);
            console.log("🏷️ Extracted Tag:", tag);

            const response = await fetch("/todo", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                task: taskTitle,
                tag: tag, // ✅ Ensure the tag is correctly sent
                due_date: dueDate,
                priority: priority,
              }),
            });

            if (response.ok) {
              console.log("Task added");

              // ✅ Show success message
              showTaskAddedMessage();

              // ✅ Refresh tasks and UI
              await fetchTasks();
              extractTags();
              if (currentTag) loadTasksForTag(currentTag);
              else loadTodayTasks();
            }

            // ✅ Function to show success message
            function showTaskAddedMessage() {
              const message = document.createElement("div");
              message.innerText = "✅ Task Added!";
              message.className = "task-success-message";
              document.body.appendChild(message);

              setTimeout(() => {
                message.remove(); // Remove message after 2 sec
              }, 2000);
            }
          });

        // ✅ Cancel button handler
        document
          .getElementById("cancel-add-task-button")
          .addEventListener("click", function () {
            document.getElementById("new-task-form").remove();
            document.getElementById("new-task-button").style.display =
              "inline-block";
          });
      });
  }

  // ✅ Sidebar filter buttons
  document
    .querySelector('[data-category="today"]')
    .addEventListener("click", loadTodayTasks);

  document
    .querySelector('[data-category="upcoming"]')
    .addEventListener("click", loadUpcomingTasks);

  document
    .querySelector('[data-category="viewAll"]')
    .addEventListener("click", function () {
      currentTag = "";
      renderTasks(allTasks, "All Tasks");
    });

  // ✅ Load today's tasks on startup
  loadTodayTasks();
});

