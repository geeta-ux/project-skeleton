from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from .. import db
from ..models.user import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# ===== REGISTER =====
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        if User.query.filter_by(email=email).first():
            flash("Email already exists.", "danger")
            return redirect(url_for("auth.register"))

        user = User(name=name, email=email)
        user.set_password(password)  # 🔑 hash the password
        db.session.add(user)
        db.session.commit()

        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


# ===== LOGIN =====
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash("Invalid email or password.", "danger")
            return redirect(url_for("auth.login"))

        login_user(user)
        flash("Logged in successfully!", "success")
        # Redirect to dashboard (you can later change this to main.index if you create main blueprint)
        return redirect(url_for("auth.dashboard"))

    return render_template("auth/login.html")


# ===== DASHBOARD =====
@auth_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("auth/dashboard.html", user=current_user)


# ===== LOGOUT =====
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", "success")
    return redirect(url_for("auth.login"))
