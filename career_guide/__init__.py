from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from datetime import datetime


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
migrate = Migrate()  # Initialize Flask-Migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)  # Attach migrate to app and db

    # Import blueprints inside the app context
    with app.app_context():
        from career_guide.routes.auth import auth_bp
        from career_guide.routes.main import main_bp
        from career_guide.routes.admin import admin_bp
        from career_guide.routes.dev import dev_bp
        from career_guide.routes.assess import assess_bp
        # Register blueprints
        app.register_blueprint(auth_bp)
        app.register_blueprint(main_bp)
        app.register_blueprint(admin_bp)
        app.register_blueprint(dev_bp)
        app.register_blueprint(assess_bp)


        # Create tables if they don't exist (optional)
        db.create_all()
        @app.context_processor
        def inject_now():
         return {'now': datetime.utcnow}

    # Flask-Login user loader
    @login_manager.user_loader
    def load_user(user_id):
        from career_guide.models.user import User
        return User.query.get(int(user_id))

    return app
