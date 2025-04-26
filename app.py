# app.py
from flask import Flask, redirect, url_for
from db import db
from extensions import login_manager

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '3fa85f64a3b1343cc3a6d5b5b5d3e7f1a2c4e5f67890abc123456def7890123'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///roomieconnect.db'
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # Import and register blueprints
    from auth import auth_bp
    from main import main_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    
    # Simple root route that redirects to login
    @app.route('/')
    def root():
        return redirect(url_for('auth.login'))
    
    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)