from models import db, User, ToDo, CalendarEvent
from app import app
from datetime import datetime

with app.app_context():
    db.drop_all()  # Optional: Reset the database (only use if you want a fresh start)
    db.create_all()

    # ========== Add Test Users ==========

    user = User(user_id = 2, username = "user1", password = "password1", full_name = "user1")
    db.session.add_all([user])
    db.session.commit()  # Commit so we can use their user_ids

    # ========== Add To-Do Tasks ==========
    tasks = [
        # User 1 - 3 Tasks
        ToDo(user_id=user.user_id, task="Complete Flask API", is_completed=False, due_date=datetime(2024, 2, 22), priority="High"),
        ToDo(user_id=user.user_id, task="Prepare for project demo", is_completed=False, priority="Medium"),
        ToDo(user_id=user.user_id, task="Write project report", is_completed=False, due_date=datetime(2024, 2, 25), priority="High"),

        # User 2 - 2 Tasks
        #ToDo(user_id=user2.user_id, task="Read database documentation", is_completed=True, priority="Low"),
        #ToDo(user_id=user2.user_id, task="Fix front-end bug", is_completed=False, priority="Medium"),

        # User 3 - 1 Task
        #ToDo(user_id=user3.user_id, task="Set up GitLab repository", is_completed=False, priority="High"),
    ]
    db.session.add_all(tasks)

    # ========== Add Calendar Events ==========
    events = [
        # User 1 - 2 Events
        CalendarEvent(user_id=user.user_id, title="Team Meeting", description="Discuss project progress", start_time=datetime(2024, 2, 23, 10, 0), end_time=datetime(2024, 2, 23, 12, 0)),
        CalendarEvent(user_id=user.user_id, title="Code Review Session", description="Review team members' code", start_time=datetime(2024, 2, 24, 14, 0), end_time=datetime(2024, 2, 24, 16, 0)),

        # User 2 - 3 Events
        #CalendarEvent(user_id=user2.user_id, title="Backend API Testing", description="Test API endpoints and bug fixes", start_time=datetime(2024, 2, 26, 9, 0), end_time=datetime(2024, 2, 26, 11, 0)),
        #CalendarEvent(user_id=user2.user_id, title="Database Optimization", description="Optimize database queries", start_time=datetime(2024, 2, 27, 13, 0), end_time=datetime(2024, 2, 27, 15, 0)),
        #CalendarEvent(user_id=user2.user_id, title="Team Presentation", description="Present project updates", start_time=datetime(2024, 2, 28, 10, 0), end_time=datetime(2024, 2, 28, 12, 0)),

        # User 3 - 1 Event
        #CalendarEvent(user_id=user3.user_id, title="Final Project Submission", description="Submit final project documents", start_time=datetime(2024, 3, 1, 17, 0), end_time=datetime(2024, 3, 1, 18, 0)),
    ]
    db.session.add_all(events)

    db.session.commit()

    print("✅ Test data inserted successfully!")
