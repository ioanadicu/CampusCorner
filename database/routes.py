import datetime
import math
from flask import Blueprint, make_response, request, jsonify, redirect, session, url_for, render_template
from models import db, ToDo, CalendarEvent
import re
import itsdangerous
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

def check_referrer(referer):
    if referer == None:
        return False
    if '/auth/user' in referer:
        return True
    return False

# ========================
# To-Do List
# ========================

# Serve the To-Do page (renders todo.html)
@routes.route('/todo', methods=['GET'])
@login_required
def todo_page():
    referer = request.headers.get('Referer')
    if check_referrer(referer):
        return render_template('todo.html')
    return "You can't access this page", 403
    

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
    referer = request.headers.get('Referer')
    print('request from', referer)
    if check_referrer(referer):
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
    return "You can't access this page", 403
    
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
    referer = request.headers.get('Referer')
    if check_referrer(referer):
        return render_template('wellbeing.html')
    return "You can't access this page", 403

@routes.route('/event', methods=['GET'])
@login_required
def event_description():
    referer = request.headers.get('Referer')
    if check_referrer(referer):
        return render_template('event.html')
    return "You can't access this page", 403


@routes.route('/cat', methods=['GET'])
@login_required
def cat():
    referer = request.headers.get('Referer')
    if check_referrer(referer):
        return render_template('cat.html')
    return "You can't access this page", 403

@routes.route('/score', methods=['GET'])
@login_required
def get_score():
    print('current score is', SCORE)
    return str(SCORE)

SHOP = {'Milk':2, 'Fish':5}
@routes.route('/feed_cat', methods=['GET'])
@login_required
def feed_cat():
    referer = request.headers.get('Referer')
    if check_referrer(referer):
        global SCORE
        food = request.args.get('food')
        print('bought', food)
        if food in SHOP.keys():
            SCORE -= SHOP[food]
        return str(SCORE)
    return "You can't access this page", 403

USER_ID = 123
@routes.route('/navigation', methods=['GET'])
@login_required
def qr_code():
    import qr_generator
    img_base64 = qr_generator.generate_qr_code_base64(session["user_id"])  # Generate base64 image
    return render_template('QR_for_AR.html', qr_code_base64=img_base64)

@routes.route('/scan')
def scan_qr_code():
    token = request.args.get('token')

    if token:
        try:
            # Verify and decode the token
            import qr_generator
            user_id = qr_generator.signer.loads(token, max_age=3600)  # 1 hour expiration for the token
            response = make_response(render_template('test_qr.html'))
            response.set_cookie('user_id', str(user_id), httponly=True, secure=True, samesite='Lax')  # Set the cookie with user ID
            print('this is user', str(user_id))
            return response

        except itsdangerous.SignatureExpired:
            return "The link has expired, please try again.", 400
        except itsdangerous.BadSignature:
            return "Invalid token, please try again.", 400
    else:
        return "No token found.", 400
    



buildings = {'Kilburn':[53.467, -2.234], 'Engineering':[53.469,-2.234], 'Library':[53.464, -2.235], 'Simon':[53.466, -2.232], 'Woolton':[53.443, -2.215]}
NAV_HISTORY = []


@routes.route('/building', methods=['GET', 'POST'])
def show_building():
    if request.method == 'POST':
        building = request.form.get('building')
        initLat = float(request.form.get('lat'))
        initLon = float(request.form.get('lon'))
        compass = float(request.form.get('angle'))

        direction = determine_direction(initLat, initLon, building, compass)
        print(building, initLat, initLon, compass)
        print(building, buildings[building])
        print(direction)
        lat = buildings[building][0]
        lon = buildings[building][1]
        if direction == 'back':
            lat -= 0.001
        elif direction == 'forward':
            lat += 0.001
        elif direction == 'left':
            lon -= 0.001
        elif direction == 'right':
            lon += 0.001
        if building in list(buildings.keys()):
            coords = "latitude:"+str(lat)+"; longitude:"+str(lon)
            return render_template('camera.html', coords = coords, name = building)

def calculate_bearing(lat1, lon1, lat2, lon2):
    # Convert degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Formula to calculate the bearing
    delta_lon = lon2_rad - lon1_rad
    x = math.sin(delta_lon) * math.cos(lat2_rad)
    y = math.cos(lat1_rad) * math.sin(lat2_rad) - math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(delta_lon)

    # Calculate the bearing (in degrees)
    initial_bearing = math.atan2(x, y)

    # Convert to degrees and normalize to 0-360 degrees
    initial_bearing_deg = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing_deg + 360) % 360

    return compass_bearing

def determine_direction(initial_lat, initial_lon, building, compass_angle):
    # Get destination coordinates from dictionary
    destination_lat, destination_lon = buildings[building]

    # Calculate the bearing to the destination
    bearing_to_destination = calculate_bearing(initial_lat, initial_lon, destination_lat, destination_lon)

    # Normalize the compass heading
    compass_angle = compass_angle % 360

    # Determine relative direction
    angle_diff = (bearing_to_destination - compass_angle + 360) % 360

    # Check the direction (left, right, forward, or back)
    if 45 <= angle_diff < 135:
        return "right"
    elif 135 <= angle_diff < 225:
        return "back"
    elif 225 <= angle_diff < 315:
        return "left"
    else:
        return "forward"
