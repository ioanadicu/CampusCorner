from flask import Blueprint, request, jsonify
from models import ToDoList
from app import db
from datetime import datetime

# Define a blueprint with a URL prefix for all to-do related routes
todo_bp = Blueprint('todo', __name__, url_prefix='/todo')

# GET endpoint: View all tasks
@todo_bp.route('/', methods=['GET'])
def get_tasks():
    tasks = ToDoList.query.all()  # Fetch all tasks from the database
    task_list = [
        {
            'taskid': task.taskid,
            'userid': task.userid,
            'task': task.task,
            'iscompleted': task.iscompleted,
            'duedate': str(task.duedate) if task.duedate else None,
            'priority': task.priority,
            'category': task.category,
            'createdat': str(task.createdat),
            'updatedat': str(task.updatedat)
        }
        for task in tasks
    ]
    return jsonify(task_list), 200

# POST endpoint: Add a new task
@todo_bp.route('/', methods=['POST'])
def add_task():
    data = request.get_json()
    try:
        # Convert userid to int
        userid = int(data['userid'])
        
        # Parse the duedate string into a date object if provided
        duedate_str = data.get('duedate')
        if duedate_str:
            duedate = datetime.strptime(duedate_str, "%Y-%m-%d").date()
        else:
            duedate = None

        # Set priority and category to None if empty strings are provided
        priority = data.get('priority') if data.get('priority') else None
        category = data.get('category') if data.get('category') else None

        new_task = ToDoList(
            userid=userid,
            task=data['task'],
            iscompleted=data.get('iscompleted', False),
            duedate=duedate,
            priority=priority,
            category=category,
            createdat=datetime.utcnow(),
            updatedat=datetime.utcnow()
        )
        db.session.add(new_task)
        db.session.commit()
        return jsonify({"message": "Task added successfully", "taskid": new_task.taskid}), 201
    except Exception as e:
        db.session.rollback()
        print("Error adding task:", e)  # This prints the error to your terminal
        return jsonify({"error": str(e)}), 400

# DELETE endpoint: Remove a task by its ID
@todo_bp.route('/<int:taskid>', methods=['DELETE'])
def delete_task(taskid):
    task = ToDoList.query.get(taskid)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    try:
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Task deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


# Registeration route 

##@todo_bp.route('/register',methods=['GET','POST'])
##def register():
  ##  if request.method =='POST':
  # ##   