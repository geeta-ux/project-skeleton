from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from career_guide.models.career import Career
from career_guide.models.question import Question
from career_guide import db

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# Custom admin decorator
def admin_required(f):
    from functools import wraps

    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash("Admin access required", "danger")
            return redirect(url_for("main.index"))
        return f(*args, **kwargs)
    return decorated_function


# ------- Dashboard -------
@admin_bp.route("/")
@admin_required
def dashboard():
    return render_template("admin/dashboard.html")


# ------- Career CRUD -------
@admin_bp.route("/careers", methods=["GET", "POST"])
@login_required
@admin_required
def careers():
    if request.method == "POST":
        action = request.form.get("action")

        if action == "add":
            title = request.form.get("title")
            track = request.form.get("track")
            skills = request.form.get("skills")  # JSON string
            description = request.form.get("description")
            avg_salary_range = request.form.get("avg_salary_range")
            sample_roles = request.form.get("sample_roles")  # JSON string

            career = Career(
                title=title,
                track=track,
                skills=skills,
                description=description,
                avg_salary_range=avg_salary_range,
                sample_roles=sample_roles
            )
            db.session.add(career)
            db.session.commit()
            flash("Career added successfully!", "success")
            return redirect(url_for("admin.careers"))

        elif action == "edit":
            career_id = int(request.form.get("career_id"))
            career = Career.query.get_or_404(career_id)
            career.title = request.form.get("title")
            career.track = request.form.get("track")
            career.skills = request.form.get("skills")
            career.description = request.form.get("description")
            career.avg_salary_range = request.form.get("avg_salary_range")
            career.sample_roles = request.form.get("sample_roles")
            db.session.commit()
            flash("Career updated successfully!", "success")
            return redirect(url_for("admin.careers"))

        elif action == "delete":
            career_id = int(request.form.get("career_id"))
            career = Career.query.get_or_404(career_id)
            db.session.delete(career)
            db.session.commit()
            flash("Career deleted successfully!", "success")
            return redirect(url_for("admin.careers"))

    all_careers = Career.query.all()
    return render_template("admin/careers.html", careers=all_careers)



# ------- Question CRUD -------
@admin_bp.route("/questions", methods=["GET", "POST"])
@login_required
@admin_required
def questions():
    from flask import request

    # Handle Add Question
    if request.method == "POST" and request.form.get("action") == "add":
        text = request.form["text"]
        section = request.form.get("section")
        difficulty = request.form.get("difficulty")
        options = request.form.get("options")
        correct_option = request.form.get("correct_option")
        weight = request.form.get("weight", 1.0)

        question = Question(
            section=section,
            difficulty=difficulty,
            text=text,
            options=options,
            correct_option=correct_option,
            weight=weight
        )
        db.session.add(question)
        db.session.commit()
        flash("Question added successfully!", "success")
        return redirect(url_for("admin.questions"))

    # Handle Edit Question
    if request.method == "POST" and request.form.get("action") == "edit":
        q_id = int(request.form.get("question_id"))
        question = Question.query.get_or_404(q_id)
        question.section = request.form.get("section")
        question.difficulty = request.form.get("difficulty")
        question.text = request.form.get("text")
        question.options = request.form.get("options")
        question.correct_option = request.form.get("correct_option")
        question.weight = request.form.get("weight", 1.0)
        db.session.commit()
        flash("Question updated successfully!", "success")
        return redirect(url_for("admin.questions"))

    # Handle Delete Question
    if request.method == "POST" and request.form.get("action") == "delete":
        q_id = int(request.form.get("question_id"))
        question = Question.query.get_or_404(q_id)
        db.session.delete(question)
        db.session.commit()
        flash("Question deleted successfully!", "success")
        return redirect(url_for("admin.questions"))

    all_questions = Question.query.all()
    return render_template("admin/questions.html", questions=all_questions)
