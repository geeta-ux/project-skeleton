from flask import Blueprint, redirect, url_for, flash
from flask_login import login_user
from career_guide.models.user import User

dev_bp = Blueprint("dev", __name__, url_prefix="/dev")

@dev_bp.route("/login_admin")
def login_admin():
    # Get first admin user
    admin = User.query.filter_by(is_admin=True).first()
    if not admin:
        return "Admin user does not exist. Create one first.", 400

    # Log in admin
    login_user(admin)
    flash("Logged in as admin!", "success")
    return redirect(url_for("admin.dashboard"))
