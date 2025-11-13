import io
from flask import render_template
from xhtml2pdf import pisa
from .planning import map_scores_to_tracks, generate_5year_plan


def generate_plan_pdf(result):
    """
    Generate a complete PDF report combining track mapping + 5-year roadmap.
    """
    # Extract scores from result (assuming it's JSON/dict-like)
    scores = result.scores if isinstance(result.scores, dict) else {}

    # --- Derive tracks and plan
    track_info = map_scores_to_tracks(scores)
    plan = generate_5year_plan(
        primary_track=track_info["primary_track"],
        chosen_career=result.primary_track or track_info["primary_track"],
        scores=scores
    )

    # --- Render a PDF-friendly HTML report
    html = render_template(
        "results/plan.html",
        result=result,
        user=result.user,
        scores=scores,
        track_info=track_info,
        plan=plan,
        primary_track=track_info["primary_track"],
        secondary_track=track_info["secondary_track"],
        created_at=result.created_at.strftime("%B %d, %Y"),
    )

    # --- Convert HTML → PDF
    pdf_io = io.BytesIO()
    pisa_status = pisa.CreatePDF(io.StringIO(html), dest=pdf_io, encoding='utf-8')

    if pisa_status.err:
        print("[ERROR] Failed to create PDF:", pisa_status.err)
        return None

    pdf_io.seek(0)
    return pdf_io.getvalue()
