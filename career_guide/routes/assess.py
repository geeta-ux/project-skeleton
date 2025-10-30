from flask import (
    Blueprint, json, render_template, request,
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


assess_bp = Blueprint("assess", __name__, url_prefix="/assess")

SECTIONS = ["logical", "numerical", "verbal", "creative", "empathy"]


# ---- START ASSESSMENT ----
@assess_bp.route("/start")
@login_required
def start():
    """Create a new assessment for the logged-in user"""
    assessment = Assessment(user_id=current_user.id, started_at=datetime.utcnow())
    db.session.add(assessment)
    db.session.commit()

    session["assessment_id"] = assessment.id
    flash("Assessment started!", "info")
    return redirect(url_for("assess.section", name="logical", assessment_id=assessment.id))


# ---- SECTION PAGE ----
@assess_bp.route("/section/<name>")
@login_required
def section(name):
    assessment_id = request.args.get("assessment_id") or session.get("assessment_id")
    section_name = name.lower()

    questions = Question.query.filter_by(section=section_name).all()

    for q in questions:
        try:
            if isinstance(q.options, str):
                q.options = json.loads(q.options)
        except Exception as e:
            print(f"Error parsing options for question {q.id}: {e}")
            q.options = []

    next_section = None
    if section_name in SECTIONS:
        idx = SECTIONS.index(section_name)
        if idx + 1 < len(SECTIONS):
            next_section = SECTIONS[idx + 1]

    return render_template(
        "assess/section.html",
        section_name=section_name,
        questions=questions,
        assessment_id=assessment_id,
        next_section=next_section
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
            answer=answer,
            user_id=current_user.id
        )
        db.session.add(response)
    else:
        response.selected_option = answer

    db.session.commit()
    return jsonify({"status": "ok"})


# ---- SUBMIT SECTION ----
@assess_bp.route("/submit", methods=["POST"])
@login_required
def submit_section():
    """Handle section submission → save answers → move to next or finish"""
    assessment_id = session.get("assessment_id")
    current_section = request.form.get("current_section", "").lower()

    if not assessment_id or not current_section:
        flash("Invalid submission. Please restart assessment.", "warning")
        return redirect(url_for("assess.start"))

    # ✅ Save responses for current section
    for key, value in request.form.items():
        if key.startswith("q_"):  # e.g., q_1, q_2
            qid = int(key.split("_")[1])
            response = Response.query.filter_by(
                assessment_id=assessment_id, question_id=qid
            ).first()
            if not response:
                response = Response(
                    assessment_id=assessment_id,
                    question_id=qid,
                    answer=value,
                    user_id=current_user.id
                )
                db.session.add(response)
            else:
                response.selected_option = value

    db.session.commit()

    # ✅ Find next section
    if current_section not in SECTIONS:
        flash("Invalid section name.", "danger")
        return redirect(url_for("assess.start"))

    idx = SECTIONS.index(current_section)
    if idx + 1 < len(SECTIONS):
        next_section = SECTIONS[idx + 1]
        flash(f"Section '{current_section.capitalize()}' submitted! Moving to {next_section.capitalize()} section.", "info")
        return redirect(url_for("assess.section", name=next_section, assessment_id=assessment_id))

    # ✅ All sections completed → finalize assessment
    flash("All sections completed! Generating your results...", "success")

    user_id = current_user.id
    scores = calculate_scores(user_id, assessment_id)
    track_info = map_scores_to_tracks(scores)

    result = Result.query.filter_by(user_id=current_user.id, assessment_id=assessment_id).first()

    if not result:
      result = Result(
        user_id=current_user.id,
        assessment_id=assessment_id,
        scores=scores,  # ✅ Save scores JSONB
        primary_track=track_info.get("primary_track"),
        secondary_track=track_info.get("secondary_track"),
        created_at=datetime.utcnow()
    )
      db.session.add(result)
    else:
      result.scores = scores  # ✅ Update scores if re-submitted
      result.primary_track = track_info.get("primary_track")
      result.secondary_track = track_info.get("secondary_track")

    db.session.commit()

# ✅ Render summary page
    return render_template(
    "results/summary.html",
    scores=scores,
    track_info=track_info,
    user=current_user
)