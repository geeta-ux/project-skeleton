from flask import (
    Blueprint, render_template, redirect, url_for, flash, request, session
)
from flask_login import login_user, login_required, logout_user, current_user
from career_guide import db
from career_guide.models.user import User

# Google OAuth imports
import os
import json
import pathlib
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
import google.auth.transport.requests

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# ===== Google OAuth Setup =====
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # For local testing only

BASE_DIR = pathlib.Path(__file__).parent.parent
CLIENT_SECRETS_FILE = os.path.join(BASE_DIR, "secrets", "client_secret.json")

# Load client ID from JSON
with open(CLIENT_SECRETS_FILE, "r") as f:
    client_data = json.load(f)["web"]
    GOOGLE_CLIENT_ID = client_data["client_id"]

flow = Flow.from_client_secrets_file(
    client_secrets_file=CLIENT_SECRETS_FILE,
    scopes=["https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/auth/callback"
)

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
        user.set_password(password)
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
        return redirect(url_for("auth.dashboard"))

    # Add "Login with Google" link on page
    return render_template("auth/login.html")

# ===== Google Login Start =====
@auth_bp.route("/google_login")
def google_login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

# ===== Google OAuth Callback =====
@auth_bp.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    request_session = google.auth.transport.requests.Request()
    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=request_session,
        audience=GOOGLE_CLIENT_ID
    )

    email = id_info.get("email")
    name = id_info.get("name")

    # If user doesn't exist, auto-create
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(name=name, email=email, is_admin=False)
        # No password since Google handles auth
        db.session.add(user)
        db.session.commit()

    login_user(user)
    flash(f"Logged in as {name}", "success")
    return redirect(url_for("auth.dashboard"))

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
