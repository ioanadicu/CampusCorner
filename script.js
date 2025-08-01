document.addEventListener("DOMContentLoaded", function () {
    console.log("Script loaded successfully!");

    /*************** Global Data & Helpers ***************/
    const allTasks = [];
    let currentCategory = "";

    function getTodayStr() {
        const today = new Date();
        const yyyy = today.getFullYear();
        const mm = String(today.getMonth() + 1).padStart(2, '0');
        const dd = String(today.getDate()).padStart(2, '0');
        return `${yyyy}-${mm}-${dd}`;
    }

    /*************** Show & Hide To-Do List Modal ***************/
    const openTodoBtn = document.getElementById("open-todo");
    const todoContainer = document.getElementById("todo-container");
    const closeTodoBtn = document.getElementById("close-todo");

    openTodoBtn.addEventListener("click", function () {
        todoContainer.style.display = "block";
    });

    closeTodoBtn.addEventListener("click", function () {
        todoContainer.style.display = "none";
    });

    function getFilteredTasks(key) {
        const todayStr = getTodayStr();
        if (key === "today") {
            return allTasks.filter(task => task.dueDate === todayStr);
        } else if (key === "upcoming") {
            return allTasks.filter(task => task.dueDate >= todayStr).sort((a, b) => a.dueDate.localeCompare(b.dueDate));
        } else {
            return allTasks.filter(task => task.category === key);
        }
    }

    /*************** Function to Attach Click Event to Categories ***************/
    function attachCategoryClick(elem) {
        elem.addEventListener("click", function () {
            document.querySelectorAll(".category").forEach(cat => cat.classList.remove("active"));
            elem.classList.add("active");
            updateContent(elem.getAttribute("data-category"), elem.textContent);
        });
    }

    document.querySelectorAll(".category").forEach(attachCategoryClick);

    document.getElementById("add-category-btn").addEventListener("click", function () {
        const newCategoryName = prompt("Enter new category name:");
        if (newCategoryName) {
            const key = newCategoryName.trim().toLowerCase().replace(/\s+/g, "-");

            if (document.querySelector(`[data-category="${key}"]`)) {
                alert("Category already exists!");
                return;
            }

            const newCatElem = document.createElement("div");
            newCatElem.className = "category";
            newCatElem.setAttribute("data-category", key);
            newCatElem.textContent = newCategoryName;

            attachCategoryClick(newCatElem);
            document.getElementById("custom-category-list").appendChild(newCatElem);
            
            // Update the content to reflect the newly created category
            updateContent(key, newCategoryName);
        }
    });

    /*************** Function to Update Content ***************/
    function updateContent(key, displayName) {
        currentCategory = key;
        const content = document.getElementById("content");
        const filteredTasks = getFilteredTasks(key);

        let html = `<h1>${displayName}</h1><ul id="task-list">`;

        if (filteredTasks.length === 0) {
            html += `<li>No tasks yet.</li>`;
        } else {
            filteredTasks.forEach(task => {
                html += `
                    <li data-id="${task.id}">
                        <span class="delete-bullet">&#x2022;</span>
                        <div class="task-details">
                            <div class="task-text">${task.text}</div>
                            <div class="task-date">${task.dueDate}</div>
                        </div>
                    </li>
                `;
            });
        }

        html += `</ul>`;

        // Only add the "New Task" button for custom categories
        if (key !== "today" && key !== "upcoming") {
            html += `<button id="new-task-button">New Task</button>`;
        }

        content.innerHTML = html;
        attachTaskDeletionHandlers();
        
        if (key !== "today" && key !== "upcoming") {
            attachNewTaskButtonHandler(displayName);
        }
    }

    /*************** Attach Event Listeners to Task Deletion ***************/
    function attachTaskDeletionHandlers() {
        document.querySelectorAll(".delete-bullet").forEach(bullet => {
            bullet.addEventListener("click", function (e) {
                e.stopPropagation();
                const li = this.parentElement;
                const taskId = li.getAttribute("data-id");
                const index = allTasks.findIndex(task => task.id == taskId);
                if (index !== -1) {
                    allTasks.splice(index, 1);
                    updateContent(currentCategory, document.querySelector(".category.active")?.textContent || "");
                }
            });
        });
    }

    /*************** Attach Event Listener to New Task Button ***************/
    function attachNewTaskButtonHandler(displayName) {
        document.getElementById("new-task-button").addEventListener("click", function () {
            showNewTaskForm(displayName);
        });
    }

    /*************** Function to Show New Task Form ***************/
    function showNewTaskForm(displayName) {
        const content = document.getElementById("content");
        const newTaskButton = document.getElementById("new-task-button");
        newTaskButton.style.display = "none";

        const formHTML = `
            <div id="new-task-form">
                <input type="text" id="new-task-text" placeholder="Reminder name">
                <input type="date" id="new-task-date" value="${getTodayStr()}">
                <button id="confirm-add-task-button">Add Task</button>
                <button id="cancel-add-task-button">Cancel</button>
            </div>
        `;

        newTaskButton.insertAdjacentHTML("afterend", formHTML);

        document.getElementById("confirm-add-task-button").addEventListener("click", function () {
            const taskText = document.getElementById("new-task-text").value.trim();
            const taskDate = document.getElementById("new-task-date").value;

            if (!taskText) {
                alert("Please enter a reminder name.");
                return;
            }
            if (!taskDate) {
                alert("Please select a due date.");
                return;
            }

            const newTask = {
                id: Date.now(),
                category: currentCategory,
                text: taskText,
                dueDate: taskDate
            };

            allTasks.push(newTask);
            updateContent(currentCategory, displayName);
        });

        document.getElementById("cancel-add-task-button").addEventListener("click", function () {
            document.getElementById("new-task-form").remove();
            newTaskButton.style.display = "inline-block";
        });
    }
});
