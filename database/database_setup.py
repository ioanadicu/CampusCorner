from models import db, User, ToDo, CalendarEvent
from app import app
from datetime import datetime

########################################################################

# DATABASE SETUP FILE FOR TESTING 
# ADDS TEST VALUES FOR CALENDAR AND TO-DO FOR USERID=1 

################################################################   

with app.app_context():
    db.drop_all()  # Clears database 
    db.create_all()  # Creates tables

    # ========== Add Test Users ==========
    test_user = User(
        user_id=1,  # Manually setting user_id (auto-incrementing continues from here)
        username="c7f437",
        password="123",  
        fullname = "Mohammed Raja ",
        role_id=None  
    )

    db.session.add(test_user)
    db.session.commit()  # Commit so we can use user_id

    # ========== Add To-Do Tasks ==========
    tasks = [
        ToDo(user_id=test_user.user_id, task="Complete Flask API", is_completed=False, due_date=datetime(2024, 2, 22), priority="High"),
        ToDo(user_id=test_user.user_id, task="Prepare for project demo", is_completed=False, priority="Medium"),
        ToDo(user_id=test_user.user_id, task="Write project report", is_completed=False, due_date=datetime(2024, 2, 25), priority="High"),
    ]
    db.session.add_all(tasks)

    # ========== Add Calendar Events ==========
    events = [
        CalendarEvent(user_id=test_user.user_id, title="Team Meeting", description="Discuss project progress",
                      start_time=datetime(2024, 2, 23, 10, 0), end_time=datetime(2024, 2, 23, 12, 0), location="Room 101"),
        CalendarEvent(user_id=test_user.user_id, title="Code Review Session", description="Review team members' code",
                      start_time=datetime(2024, 2, 24, 14, 0), end_time=datetime(2024, 2, 24, 16, 0), location="Library"),
    ]
    db.session.add_all(events)

    db.session.commit()

    print("✅ Test data inserted successfully!")
