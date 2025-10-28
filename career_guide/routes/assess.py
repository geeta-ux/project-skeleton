# career_guide/routes/assess.py
from flask import (
    Blueprint, render_template, request,
    redirect, url_for, jsonify, flash, session
)
from flask_login import login_required, current_user
from datetime import datetime

from career_guide import db
from career_guide.models.assessment import Assessment
from career_guide.models.response import Response
from career_guide.models.result import Result
from career_guide.models.question import Question
from career_guide.services.scoring import calculate_scores
from career_guide.services.planning import map_scores_to_tracks


# ✅ single consistent blueprint
assess_bp = Blueprint("assess", __name__, url_prefix="/assess")


# ---- START ASSESSMENT ----
@assess_bp.route("/start")
@login_required
def start():
    """Create a new assessment for the logged-in user"""
    assessment = Assessment(user_id=current_user.id, started_at=datetime.utcnow())
    db.session.add(assessment)
    db.session.commit()

    # store in session for subsequent routes
    session["assessment_id"] = assessment.id

    flash("Assessment started!", "info")
    return redirect(url_for("assess.section", name="aptitude", assessment_id=assessment.id))


# ---- SECTION PAGE ----
@assess_bp.route("/section/<name>")
@login_required
def section(name):
    """Render a section with its questions"""
    assessment_id = request.args.get("assessment_id") or session.get("assessment_id")

    if not assessment_id:
        flash("No active assessment found.", "warning")
        return redirect(url_for("assess.start"))

    assessment = Assessment.query.get_or_404(assessment_id)
    questions = Question.query.filter_by(section=name).all()

    return render_template(
        "assess/section.html",
        section=name,
        questions=questions,
        assessment_id=assessment.id,
        user=current_user
    )


# ---- AUTOSAVE (AJAX) ----
@assess_bp.route("/autosave", methods=["POST"])
@login_required
def autosave():
    """Autosave each response asynchronously"""
    data = request.get_json()
    assessment_id = data.get("assessment_id") or session.get("assessment_id")
    qid = data.get("question_id")
    answer = data.get("answer")

    if not (assessment_id and qid and answer):
        return jsonify({"status": "error", "message": "Incomplete data"}), 400

    response = Response.query.filter_by(
        assessment_id=assessment_id, question_id=qid
    ).first()

    if not response:
        response = Response(
            assessment_id=assessment_id,
            question_id=qid,
            selected_option=answer,
            user_id=current_user.id  # ✅ tie response to current user
        )
        db.session.add(response)
    else:
        response.selected_option = answer

    db.session.commit()
    return jsonify({"status": "ok"})


# ---- SUBMIT ----
@assess_bp.route("/submit", methods=["POST"])
@login_required
def submit_assessment():
    """Finalize assessment → score → map → results"""
    user_id = current_user.id
    assessment_id = session.get("assessment_id")

    if not assessment_id:
        flash("No active assessment session found.", "warning")
        return redirect(url_for("assess.start"))

    # 1️⃣ Compute normalized section scores
    scores = calculate_scores(user_id, assessment_id)

    # 2️⃣ Map scores → career tracks
    track_info = map_scores_to_tracks(scores)

    # 3️⃣ Save to Result table
    result = Result.query.filter_by(user_id=user_id, assessment_id=assessment_id).first()
    if not result:
        result = Result(
            user_id=user_id,
            assessment_id=assessment_id,
            primary_track=track_info["primary_track"],
            secondary_track=track_info["secondary_track"],
            created_at=datetime.utcnow()
        )
        db.session.add(result)
    else:
        result.primary_track = track_info["primary_track"]
        result.secondary_track = track_info["secondary_track"]

    db.session.commit()

    # 4️⃣ Render results page
    return render_template(
        "results/summary.html",
        scores=scores,
        track_info=track_info,
        user=current_user
    )
