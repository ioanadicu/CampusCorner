import datetime
from flask import Blueprint, make_response, request, jsonify, redirect, session, url_for, render_template
from models import db, ToDo, CalendarEvent
import re

import configparser

import calendarapp
import calendarrenderer

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
    print("User ID for fetching tasks:", user_id)  # Debug print
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
CONFIG_PATH = "cal_testing_config.ini"
#CAL_LINK = 'https://scientia-eu-v4-api-d3-02.azurewebsites.net//api/ical/b5098763-4476-40a6-8d60-5a08e9c52964/a9115f76-f299-57a2-f64b-7df3c403176d/timetable.ics' #TODO this will be removed because the link will come from db
CAL_LINKS = []
CAL_OFFSET = [0, 0]
SCORE = 0
@routes.route('/calendar', methods=("GET", "POST"))
@login_required
def calendar_page():
    if len(CAL_LINKS)>0:
        calendar_app = calendarapp.CalendarApp()

        # add a calendar from url from config file
        #config = configparser.ConfigParser()
        #config.read(CONFIG_PATH)
        #calendar_app.add_calendar_from_url(str(config["Settings"]["calURL"]))
        for calendar in CAL_LINKS:
            calendar_app.add_calendar_from_url(calendar)

        renderer = calendarrenderer.CalendarRenderer(calendar_app)
        month_offset = int(request.args.get("month_offset", 0))
        renderer.month_offset = month_offset
        today = datetime.date.today()
        print('month', today.month + CAL_OFFSET[1])
        renderer.now = datetime.datetime(today.year + CAL_OFFSET[0], today.month + CAL_OFFSET[1], today.day)
        return renderer.render()
    
    #if there are no calendars render an empty calendar
    return render_template('default_calendar.html')
    
@routes.route('/add_calendar', methods=["GET"])
@login_required
def add_calendar():
        global CAL_LINKS
        regex = r'^(https?|ftp):\/\/[^\s/$.?#].[^\s]*$'
        new_calendar = request.args.get('new_calendar')
        print('new calendar: ', new_calendar)
        if new_calendar:
            if bool(re.match(regex, new_calendar)):
                CAL_LINKS.append(new_calendar)
        return redirect(url_for('routes.calendar_page'))

@routes.route('/change_month', methods=["GET"])
@login_required
def change_month():
        global CAL_OFFSET
        direction = request.args.get('direction')
        print('direction: ', direction)
        today = datetime.date.today()
        if direction == 'forward':
            if today.month + CAL_OFFSET[1] == 12:
                CAL_OFFSET[0] += 1
                CAL_OFFSET[1] -= 11
            else:
                CAL_OFFSET[1] += 1
        elif direction == 'back':
            if today.month + CAL_OFFSET[1] == 1:
                CAL_OFFSET[0]-= 1
                CAL_OFFSET[1] += 11
            else:
                CAL_OFFSET[1] -= 1
            print(CAL_OFFSET)
        return redirect(url_for('routes.calendar_page'))


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

@routes.route('/wellbeing', methods=['GET'])
@login_required
def wellbeing_folder():
    return render_template('wellbeing.html')

@routes.route('/event', methods=['GET'])
@login_required
def event_description():
    return render_template('event.html')


@routes.route('/cat', methods=['GET'])
@login_required
def cat():
    return render_template('cat.html')

@routes.route('/score', methods=['GET'])
@login_required
def get_score():
    return str(SCORE)

@routes.route('/feed_cat', methods=['GET'])
@login_required
def feed_cat():
    global SCORE
    cost = request.args.get('cost')
    print('the cost', cost)
    SCORE -= int(cost)
    return str(SCORE)



    
    

