import json
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    login_manager.login_view = "auth.login"

    with app.app_context():
        # Register blueprints
        from career_guide.routes.auth import auth_bp
        from career_guide.routes.main import main_bp
        from career_guide.routes.assess import assess_bp
        from career_guide.routes.admin import admin_bp
        from career_guide.routes.dev import dev_bp
        from career_guide.routes.results import results_bp   # ✅ add this line


        app.register_blueprint(auth_bp)
        app.register_blueprint(main_bp)
        app.register_blueprint(assess_bp)
        app.register_blueprint(admin_bp)
        app.register_blueprint(dev_bp)
        app.register_blueprint(results_bp)

        db.create_all()

        # ✅ Inject UTC time into templates
        @app.context_processor
        def inject_now():
            return {'now': datetime.utcnow}

        # ✅ Custom Jinja filter to load JSON strings (named 'loads')
        @app.template_filter("loads")
        def loads_filter(value):
            try:
                if isinstance(value, (dict, list)):
                    return value  # already JSON
                return json.loads(value)
            except (ValueError, TypeError):
                return []

    @login_manager.user_loader
    def load_user(user_id):
        from career_guide.models.user import User
        return User.query.get(int(user_id))

    return app
