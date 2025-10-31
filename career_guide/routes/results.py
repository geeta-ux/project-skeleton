from flask import Blueprint, render_template
from flask_login import login_required, current_user
from career_guide.models.result import Result
from career_guide.services.matching import get_top_careers
from career_guide.services.planning import generate_5year_plan


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

    # ✅ 1️⃣ Call the matching service
    recommended_careers = get_top_careers(result.primary_track, scores)

    plan = generate_5year_plan(result.primary_track, result.career_name, result.scores)


    # ✅ 2️⃣ Pass recommendations to the template
    return render_template(
        "results/summary.html",
        result=result,
        scores=scores,
        track_info=track_info,
        careers=recommended_careers,
        plan=plan,
        user=current_user
    )
