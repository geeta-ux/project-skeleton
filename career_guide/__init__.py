from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize extensions globally
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    from .models.user import User  # import here to avoid circular imports
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")  # or your config class

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
    from .routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    # Add other blueprints here: assess, results, admin, api

    return app
