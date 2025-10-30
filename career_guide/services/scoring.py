import numpy as np
from statistics import mean, stdev
from career_guide import db
from career_guide.models.response import Response
from career_guide.models.result import Result
from datetime import datetime



def compute_raw_scores(responses):
    """
    Compute per-section raw scores.
    responses: list of Response objects (with question.section and score)
    """
    section_scores = {}

    for r in responses:
        section = r.question.section
        
        # Calculate score from answer (you can adjust this logic)
        score = calculate_score_from_answer(r.answer)
        
        section_scores.setdefault(section, []).append(score)

    # Average per section
    return {section: mean(scores) for section, scores in section_scores.items()}


def calculate_score_from_answer(answer):
    """
    Example function to calculate a score from the answer.
    Customize this logic based on your requirements.
    """
    try:
        # Example: score based on numerical answer (you can customize this)
        return float(answer)
    except ValueError:
        return 0  # Default score for invalid answers


def normalize_scores(raw_scores, method="minmax"):
    """
    Normalize raw scores using z-score or min-max scaling.
    """
    values = list(raw_scores.values())
    if not values:
        return {}

    if method == "zscore":
        mu, sigma = mean(values), stdev(values) or 1
        return {k: round((v - mu) / sigma, 2) for k, v in raw_scores.items()}

    # Default: Min–max normalization
    min_v, max_v = min(values), max(values)
    denom = (max_v - min_v) or 1
    return {k: round((v - min_v) / denom, 2) for k, v in raw_scores.items()}


def calculate_scores(user_id, assessment_id, method="minmax"):
    """
    Main scoring pipeline for an assessment attempt.
    """
    responses = Response.query.filter_by(
        user_id=user_id, assessment_id=assessment_id
    ).all()

    if not responses:
        return {}

    raw = compute_raw_scores(responses)
    normalized = normalize_scores(raw, method)

    # Store in Results table
    result = Result.query.filter_by(user_id=user_id, assessment_id=assessment_id).first()

    if not result:
        result = Result(
            user_id=user_id,
            assessment_id=assessment_id,
            scores =normalized,  # Store normalized scores in JSONB column
            primary_track=None,  # Add the logic for tracks if needed
            secondary_track=None,
            created_at=datetime.utcnow()
        )
        db.session.add(result)
    else:
        result.scores  = normalized  # Update scores if re-submitted

    db.session.commit()

    return normalized
