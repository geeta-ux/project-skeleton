from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from career_guide.routes.dev import dev_bp


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    login_manager.init_app(app)

    # Import blueprints *inside the app context* to avoid circular imports
    with app.app_context():
        try:
            from career_guide.routes.auth import auth_bp
            from career_guide.routes.main import main_bp
            from career_guide.routes.admin import admin_bp
        except ImportError as e:
            print(f"❌ Error importing blueprints: {e}")
            raise

        # Register blueprints
        app.register_blueprint(auth_bp)
        app.register_blueprint(main_bp)
        app.register_blueprint(admin_bp)
        app.register_blueprint(dev_bp)


        # Create all database tables
        db.create_all()

    # Flask-Login user loader
    @login_manager.user_loader
    def load_user(user_id):
        from career_guide.models.user import User
        return User.query.get(int(user_id))

    return app
