from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Hashed password
    full_name = db.Column(db.String(50), nullable=False)


    tasks = db.relationship('ToDo', backref='user', lazy=True)
    events = db.relationship('CalendarEvent', backref='user', lazy=True)

# To-Do List Table
class ToDo(db.Model):
    __tablename__ = 'todo'
    
    task_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    task = db.Column(db.Text, nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.Date, nullable=True)
    priority = db.Column(db.String(10), nullable=False, default="Medium")  # Added priority
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Calendar Events Table
class CalendarEvent(db.Model):
    __tablename__ = 'calendar'
    
    event_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(100), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    is_recurring = db.Column(db.Boolean, default=False)
    recurrence_pattern = db.Column(db.String(50), nullable=True)