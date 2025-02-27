from flask import Blueprint, request, jsonify, redirect, session, url_for, render_template
from models import db, ToDo, CalendarEvent

# Blueprint for routes
routes = Blueprint("routes", __name__)


def login_required(f):
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))  # Redirect to login if not authenticated
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

# ========================
# To-Do List
# ========================

# Serve the To-Do page (renders todo.html)
@routes.route('/todo', methods=['GET'])
@login_required
def todo_page():
    return render_template('todo.html')

# Get all tasks for the logged-in user
@routes.route('/todo/tasks', methods=['GET'])
@login_required
def get_todo_tasks():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    tasks = ToDo.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "task_id": task.task_id,
        "task": task.task,
        "is_completed": task.is_completed,
        "priority": task.priority,
        "due_date": task.due_date.strftime("%Y-%m-%d") if task.due_date else None
    } for task in tasks])


# Add a new task
@routes.route('/todo', methods=['POST'])
@login_required
def add_task():
    user_id = session["user_id"]  
    data = request.json
    new_task = ToDo(
        user_id=user_id,
        task=data['task'],
        priority=data.get('priority', 'Medium'),
        due_date=data.get('due_date')
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "Task added successfully!"})

# Delete a task
@routes.route('/todo/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    user_id = session["user_id"]
    task = ToDo.query.filter_by(task_id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({"message": "Task not found or unauthorized"}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted!"})

# task completion
@routes.route('/todo/complete/<int:task_id>', methods=['PUT'])
@login_required
def complete_task(task_id):
    user_id = session["user_id"]
    task = ToDo.query.filter_by(task_id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({"message": "Task not found or unauthorized"}), 404
    data = request.json
    task.is_completed = data.get("is_completed", not task.is_completed)
    db.session.commit()
    return jsonify({"message": "Task completion status updated!"})

# Edit a task
@routes.route('/todo/<int:task_id>', methods=['PUT'])
@login_required
def update_task(task_id):
    user_id = session["user_id"]
    task = ToDo.query.filter_by(task_id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({"message": "Task not found or unauthorized"}), 404
    data = request.json
    task.task = data.get("task", task.task)
    task.priority = data.get("priority", task.priority)
    task.due_date = data.get("due_date", task.due_date)
    db.session.commit()
    return jsonify({"message": "Task updated successfully!"})

# ========================
# 📅 Calendar Routes (Moved to calendar.html)
# ========================

@routes.route('/calendar', methods=['GET'])
@login_required
def calendar_page():
    return render_template('calendar.html')

@routes.route('/calendar/events', methods=['GET'])
@login_required
def get_calendar_events():
    user_id = session["user_id"]
    events = CalendarEvent.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "event_id": e.event_id,
        "title": e.title,
        "description": e.description,
        "start_time": e.start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": e.end_time.strftime("%Y-%m-%d %H:%M:%S"),
        "location": e.location
    } for e in events])

@routes.route('/calendar', methods=['POST'])
@login_required
def add_event():
    user_id = session["user_id"]
    data = request.json
    new_event = CalendarEvent(
        user_id=user_id,
        title=data['title'],
        description=data.get('description', "No description"),
        start_time=data['start_time'],
        end_time=data['end_time'],
        location=data.get('location', "No location")
    )
    db.session.add(new_event)
    db.session.commit()
    return jsonify({"message": "Event added successfully!"})
