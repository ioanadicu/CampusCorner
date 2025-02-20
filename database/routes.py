from flask import Blueprint, request, jsonify
from models import db, ToDo, CalendarEvent

# Create a Blueprint for routes
routes = Blueprint("routes", __name__)

# ========================
# 📝 To-Do List Routes
# ========================

# Get all tasks for a user
@routes.route('/todo/<int:user_id>', methods=['GET'])
def get_todo(user_id):
    tasks = ToDo.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "task_id": t.task_id, 
        "task": t.task, 
        "is_completed": t.is_completed, 
        "priority": t.priority, 
        "due_date": t.due_date.strftime("%Y-%m-%d") if t.due_date else None
    } for t in tasks])

# Add a new task
@routes.route('/todo', methods=['POST'])
def add_task():
    data = request.json
    new_task = ToDo(
        user_id=data['user_id'],
        task=data['task'],
        priority=data.get('priority', 'Medium'),
        due_date=data.get('due_date')
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "Task added successfully!"})

# Delete a task
@routes.route('/todo/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = ToDo.query.get(task_id)
    if not task:
        return jsonify({"message": "Task not found"}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted!"})

# Toggle task completion
@routes.route('/todo/complete/<int:task_id>', methods=['PUT'])
def complete_task(task_id):
    task = ToDo.query.get(task_id)
    if not task:
        return jsonify({"message": "Task not found"}), 404
    data = request.json
    task.is_completed = data.get("is_completed", not task.is_completed)
    db.session.commit()
    return jsonify({"message": "Task completion status updated!"})

# Edit a task
@routes.route('/todo/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = ToDo.query.get(task_id)
    if not task:
        return jsonify({"message": "Task not found"}), 404

    data = request.json
    task.task = data.get("task", task.task)
    task.priority = data.get("priority", task.priority)
    task.due_date = data.get("due_date", task.due_date)
    db.session.commit()
    return jsonify({"message": "Task updated successfully!"})

# ========================
# 📅 Calendar Routes
# ========================

# Get all events for a user
@routes.route('/calendar/<int:user_id>', methods=['GET'])
def get_calendar(user_id):
    events = CalendarEvent.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "event_id": e.event_id,
        "title": e.title,
        "description": e.description,
        "start_time": e.start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": e.end_time.strftime("%Y-%m-%d %H:%M:%S")
    } for e in events])

# Add an event
@routes.route('/calendar', methods=['POST'])
def add_event():
    data = request.json
    new_event = CalendarEvent(
        user_id=data['user_id'],
        title=data['title'],
        description=data.get('description', "No description"),
        start_time=data['start_time'],
        end_time=data['end_time']
    )
    db.session.add(new_event)
    db.session.commit()
    return jsonify({"message": "Event added successfully!"})

# Delete an event
@routes.route('/calendar/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    event = CalendarEvent.query.get(event_id)
    if not event:
        return jsonify({"message": "Event not found"}), 404
    db.session.delete(event)
    db.session.commit()
    return jsonify({"message": "Event deleted!"})

# Edit an event
@routes.route('/calendar/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    event = CalendarEvent.query.get(event_id)
    if not event:
        return jsonify({"message": "Event not found"}), 404

    data = request.json
    event.title = data.get("title", event.title)
    event.description = data.get("description", event.description)
    event.start_time = data.get("start_time", event.start_time)
    event.end_time = data.get("end_time", event.end_time)
    db.session.commit()
    return jsonify({"message": "Event updated successfully!"})
