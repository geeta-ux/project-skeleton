from flask import Blueprint, render_template
from flask_login import login_required, current_user
from career_guide.models.result import Result
from career_guide.models.career import Career

bp = Blueprint("results", __name__, url_prefix="/results")

@bp.route("/<int:result_id>")
@login_required
def view(result_id):
    result = Result.query.get_or_404(result_id)
    career = Career.query.filter_by(title=result.recommended_career).first()
    return render_template("results/view.html", result=result, career=career)
