from db import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    living_preferences = db.relationship('LivingPreferences', backref='user', uselist=False)
    academic_info = db.relationship('AcademicInfo', backref='user', uselist=False)
    interests = db.relationship('Interest', secondary='user_interests', back_populates='users')
    pets_info = db.relationship('PetsInfo', backref='user', uselist=False)
    additional_preferences = db.relationship('AdditionalPreferences', backref='user', uselist=False)
    
    def get_id(self):
        return str(self.user_id)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class LivingPreferences(db.Model):
    __tablename__ = 'living_preferences'
    
    preference_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    cleanliness = db.Column(db.String(20), nullable=False)
    noise_level = db.Column(db.String(20), nullable=False)
    sleep_schedule = db.Column(db.String(20), nullable=False)
    smoking = db.Column(db.String(20), nullable=False)
    guest_frequency = db.Column(db.String(20), nullable=False)
    roommate_guest_preference = db.Column(db.String(20), nullable=False)

class AcademicInfo(db.Model):
    __tablename__ = 'academic_info'
    
    academic_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    academic_year = db.Column(db.String(20), nullable=False)
    major = db.Column(db.String(100), nullable=False)
    study_habits = db.Column(db.String(20), nullable=False)
    graduation_year = db.Column(db.Integer)

class Interest(db.Model):
    __tablename__ = 'interests'
    
    interest_id = db.Column(db.Integer, primary_key=True)
    interest_name = db.Column(db.String(50), unique=True, nullable=False)
    users = db.relationship('User', secondary='user_interests', back_populates='interests')

class UserInterests(db.Model):
    __tablename__ = 'user_interests'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    interest_id = db.Column(db.Integer, db.ForeignKey('interests.interest_id'), primary_key=True)

class PetsInfo(db.Model):
    __tablename__ = 'pets_info'
    
    pet_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    has_pets = db.Column(db.String(20), nullable=False)
    pet_details = db.Column(db.Text)

class AdditionalPreferences(db.Model):
    __tablename__ = 'additional_preferences'
    
    preference_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    additional_info = db.Column(db.Text)