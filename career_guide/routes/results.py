from io import BytesIO
import io
from flask import Blueprint, make_response, render_template
from flask_login import login_required, current_user
# from weasyprint import HTML
from xhtml2pdf import pisa
import os
from flask import Blueprint, send_file, abort
from career_guide.services.planning_service import generate_plan_pdf
from career_guide.models.result import Result
from career_guide.services.matching import get_top_careers
from career_guide.services.planning import generate_5year_plan
from career_guide.services.skill_gap import analyze_skill_gaps

results_bp = Blueprint("results", __name__, url_prefix="/results")

@results_bp.route("/<int:result_id>")
@login_required
def view_result(result_id):
    """Display a single user's result summary"""
    result = Result.query.get_or_404(result_id)

    # Extract data safely
    scores = result.scores or {}
    track_info = {
        "primary_track": result.primary_track or "N/A",
        "secondary_track": result.secondary_track or "N/A",
        "track_scores": scores,
    }

    # ✅ 1️⃣ Get top careers for the user’s primary track
    recommended_careers = get_top_careers(result.primary_track, scores)

    # ✅ 2️⃣ Generate a 5-year plan based on the top career (if available)
    top_career_title = recommended_careers[0]["career"].title if recommended_careers else None
    plan = generate_5year_plan(result.primary_track, top_career_title, scores)

    # ✅ 3️⃣ Analyze skill gaps for that top career
    gaps = analyze_skill_gaps(top_career_title or result.primary_track, scores)

    # ✅ 4️⃣ Pass everything to the results template
    return render_template(
        "results/summary.html",
        result=result,
        scores=scores,
        track_info=track_info,
        careers=recommended_careers,
        plan=plan,
        skill_gaps=gaps,
        user=current_user
    )

@results_bp.route("/download_plan/<int:result_id>")
@login_required
def download_plan(result_id):
    # Fetch result
    result = Result.query.get(result_id)
    if not result or result.user_id != current_user.id:
        abort(404)

    # Generate the plan (PDF or text)
    pdf_data = generate_plan_pdf(result)

    return send_file(
        io.BytesIO(pdf_data),
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"career_plan_{result.id}.pdf"
    )