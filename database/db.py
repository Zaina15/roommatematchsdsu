# db.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)

    sleep_schedule = db.Column(db.String(20))
    cleanliness = db.Column(db.String(20))
    social_preference = db.Column(db.String(20))
    study_habits = db.Column(db.String(20))
    guest_policy = db.Column(db.String(20))
    matching_score = db.Column(db.Float)

    def __repr__(self):
        return f'<User {self.username}>'