# auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from datetime import datetime
from db import db
from models import User, LivingPreferences, AcademicInfo, Interest, PetsInfo, AdditionalPreferences, UserInterests

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        user = User.query.filter_by(email=email).first()
        
        # Check if user exists and password is correct
        if not user or not check_password_hash(user.password_hash, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))
        
        # Update last login time
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # Login the user
        login_user(user, remember=remember)
        return redirect(url_for('main.home'))
    
    return render_template('login.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Basic user info
        email = request.form.get('email')
        password = request.form.get('password')
        username = request.form.get('username')
        full_name = request.form.get('full_name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        
        # Check if user exists
        if User.query.filter_by(email=email).first():
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))
        
        if User.query.filter_by(username=username).first():
            flash('Username already taken')
            return redirect(url_for('auth.signup'))
        
        # Create new user
        new_user = User(
            email=email,
            username=username,
            full_name=full_name,
            age=age,
            gender=gender
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        # Living preferences
        living_prefs = LivingPreferences(
            user_id=new_user.user_id,
            cleanliness=request.form.get('cleanliness'),
            noise_level=request.form.get('noise_level'),
            sleep_schedule=request.form.get('sleep_schedule'),
            smoking=request.form.get('smoking'),
            guest_frequency=request.form.get('guest_frequency'),
            roommate_guest_preference=request.form.get('roommate_guest_preference')
        )
        db.session.add(living_prefs)
        
        # Academic info
        academic_info = AcademicInfo(
            user_id=new_user.user_id,
            academic_year=request.form.get('academic_year'),
            major=request.form.get('major'),
            study_habits=request.form.get('study_habits'),
            graduation_year=request.form.get('graduation_year')
        )
        db.session.add(academic_info)
        
        # Pets info
        pets_info = PetsInfo(
            user_id=new_user.user_id,
            has_pets=request.form.get('has_pets'),
            pet_details=request.form.get('pet_details')
        )
        db.session.add(pets_info)
        
        # Additional preferences
        additional_prefs = AdditionalPreferences(
            user_id=new_user.user_id,
            additional_info=request.form.get('additional_info')
        )
        db.session.add(additional_prefs)
        
        # Interests (many-to-many)
        interests = request.form.getlist('interests')
        for interest_id in interests:
            interest = Interest.query.get(interest_id)
            if interest:
                new_user.interests.append(interest)
        
        db.session.commit()
        
        # Log the user in
        login_user(new_user)
        return redirect(url_for('main.home'))
    
    # For GET request, show empty form
    interests = Interest.query.all()
    return render_template('signup.html', interests=interests)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))