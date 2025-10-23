from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from flask_login import login_required, current_user
from career_guide.models.assessment import Assessment
from career_guide.models.response import Response
from career_guide.models.result import Result
from career_guide.models.question import Question
from career_guide.services.scoring import calculate_scores
from career_guide import db
from datetime import datetime

assess_bp = Blueprint("assess", __name__, url_prefix="/assess")

# ---- START ASSESSMENT ----
@assess_bp.route("/start")
@login_required
def start():
    # Create new assessment for this user
    assessment = Assessment(user_id=current_user.id)
    db.session.add(assessment)
    db.session.commit()
    flash("Assessment started!", "info")
    return redirect(url_for("assess.section", assessment_id=assessment.id, name="aptitude"))


# ---- SECTION PAGE ----
@assess_bp.route("/section/<name>")
@login_required
def section(name):
    assessment_id = request.args.get("assessment_id")
    assessment = Assessment.query.get_or_404(assessment_id)
    questions = Question.query.filter_by(section=name).all()

    return render_template("assess/section.html", 
                           section=name, 
                           questions=questions, 
                           assessment_id=assessment.id)


# ---- AUTOSAVE (AJAX) ----
@assess_bp.route("/autosave", methods=["POST"])
@login_required
def autosave():
    data = request.get_json()
    assessment_id = data.get("assessment_id")
    qid = data.get("question_id")
    answer = data.get("answer")

    if not (assessment_id and qid and answer):
        return jsonify({"status": "error", "message": "Incomplete data"}), 400

    response = Response.query.filter_by(assessment_id=assessment_id, question_id=qid).first()
    if not response:
        response = Response(assessment_id=assessment_id, question_id=qid, selected_option=answer)
        db.session.add(response)
    else:
        response.selected_option = answer

    db.session.commit()
    return jsonify({"status": "ok"})


# ---- SUBMIT ----
@assess_bp.route("/submit/<int:assessment_id>")
@login_required
def submit(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    responses = Response.query.filter_by(assessment_id=assessment.id).all()

    # Calculate and store result
    scores, primary, secondary = calculate_scores(responses)
    result = Result(
        assessment_id=assessment.id,
        scores=scores,
        primary_track=primary,
        secondary_track=secondary,
    )

    assessment.completed_at = datetime.utcnow()
    db.session.add(result)
    db.session.commit()

    flash("Assessment completed successfully!", "success")
    return redirect(url_for("results.view_result", result_id=result.id))
