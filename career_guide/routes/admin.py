from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from career_guide import db
from career_guide.models.career import Career
from career_guide.models.question import Question

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# Admin-only decorator
def admin_required(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_admin:
            flash("Admin access required", "danger")
            return redirect(url_for("main.index"))
        return func(*args, **kwargs)
    return login_required(wrapper)

# ----- Admin Dashboard -----
@admin_bp.route("/")
@admin_required
def dashboard():
    careers = Career.query.all()
    questions = Question.query.all()
    return render_template("admin/dashboard.html", careers=careers, questions=questions)

# ----- CRUD Careers -----
@admin_bp.route("/career/add", methods=["GET", "POST"])
@admin_required
def add_career():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        career = Career(title=title, description=description)
        db.session.add(career)
        db.session.commit()
        flash("Career added successfully", "success")
        return redirect(url_for("admin.dashboard"))
    return render_template("admin/add_career.html")

@admin_bp.route("/career/delete/<int:id>")
@admin_required
def delete_career(id):
    career = Career.query.get_or_404(id)
    db.session.delete(career)
    db.session.commit()
    flash("Career deleted", "success")
    return redirect(url_for("admin.dashboard"))

# ----- CRUD Questions -----
@admin_bp.route("/question/add", methods=["GET", "POST"])
@admin_required
def add_question():
    if request.method == "POST":
        text = request.form.get("text")
        question = Question(text=text)
        db.session.add(question)
        db.session.commit()
        flash("Question added successfully", "success")
        return redirect(url_for("admin.dashboard"))
    return render_template("admin/add_question.html")

@admin_bp.route("/question/delete/<int:id>")
@admin_required
def delete_question(id):
    question = Question.query.get_or_404(id)
    db.session.delete(question)
    db.session.commit()
    flash("Question deleted", "success")
    return redirect(url_for("admin.dashboard"))
