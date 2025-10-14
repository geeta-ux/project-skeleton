# scripts/create_admin.py
from career_guide import create_app, db
from career_guide.models.user import User

app = create_app()
with app.app_context():
    if not User.query.filter_by(email="admin@example.com").first():
        admin = User(name="Admin", email="admin@example.com", is_admin=True)
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
        print("Admin user created!")
