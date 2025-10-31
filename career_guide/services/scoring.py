import json
from statistics import mean, stdev
from datetime import datetime
from career_guide import db
from career_guide.models.response import Response
from career_guide.models.result import Result
from career_guide.services.planning import map_scores_to_tracks


# -------------------------------
# 1️⃣ Compute raw section scores
# -------------------------------
def compute_raw_scores(responses):
    # Define all the sections you expect in your assessment
    expected_sections = ["logical", "numerical", "verbal", "creative", "empathy"]
    section_scores = {section: [] for section in expected_sections}

    for r in responses:
        section = getattr(r.question, "section", None)
        if not section:
            continue

        score = calculate_score_from_answer(r.answer)
        if section in section_scores:
            section_scores[section].append(score)
        else:
            # unexpected new section (optional logging)
            print(f"[DEBUG] Unexpected section '{section}' found.")

    # Fill missing ones with zero
    return {section: (mean(scores) if scores else 0.0) for section, scores in section_scores.items()}


# -------------------------------
# 2️⃣ Convert answer → numeric
# -------------------------------
def calculate_score_from_answer(answer):
    """Convert answer (text/numeric) into a numeric score for averaging."""
    if not answer:
        return 0

    # If it's already a Python type like list/dict
    if isinstance(answer, (dict, list)):
        return 1

    # Try to interpret as JSON (e.g., if stored as '"Vague"' or similar)
    try:
        parsed = json.loads(answer)
        if isinstance(parsed, (dict, list)):
            return 1
        elif isinstance(parsed, (int, float)):
            return float(parsed)
        elif isinstance(parsed, str) and parsed.strip():
            return 1
    except (json.JSONDecodeError, TypeError):
        pass

    # If it looks like a number, use numeric value
    try:
        return float(answer)
    except (ValueError, TypeError):
        # Otherwise, count any non-empty text answer as 1
        cleaned = str(answer).strip().strip('"')
        return 1 if cleaned else 0
# -------------------------------
# 3️⃣ Normalize scores
# -------------------------------
def normalize_scores(raw_scores, method="minmax"):
    values = list(raw_scores.values())
    if not values:
        return {}

    if method == "zscore":
        mu, sigma = mean(values), stdev(values) or 1
        return {k: round((v - mu) / sigma, 2) for k, v in raw_scores.items()}

    # Min–max normalization
    min_v, max_v = min(values), max(values)
    denom = (max_v - min_v) or 1
    return {k: round((v - min_v) / denom, 2) for k, v in raw_scores.items()}


# -------------------------------
# 4️⃣ Main scoring pipeline
# -------------------------------
def calculate_scores(user_id, assessment_id, method="zscore"):
    responses = Response.query.filter_by(
        user_id=user_id, assessment_id=assessment_id
    ).all()

    if not responses:
        print(f"[DEBUG] No responses found for user {user_id}, assessment {assessment_id}")
        return {}

    # Step 1: compute raw + normalized
    raw = compute_raw_scores(responses)
    normalized = normalize_scores(raw, method)

    # Step 2: map to tracks
    track_mapping = map_scores_to_tracks(normalized)

    # Step 3: log debug info
    print(f"\n[DEBUG] RAW SCORES: {raw}")
    print(f"[DEBUG] NORMALIZED: {normalized}")
    print(f"[DEBUG] TRACK MAPPING: {track_mapping}\n")

    # Step 4: update DB
    result = Result.query.filter_by(user_id=user_id, assessment_id=assessment_id).first()
    if not result:
        result = Result(
            user_id=user_id,
            assessment_id=assessment_id,
            scores=normalized,
            primary_track=track_mapping.get("primary_track"),
            secondary_track=track_mapping.get("secondary_track"),
            created_at=datetime.utcnow(),
        )
        db.session.add(result)
    else:
        result.scores = normalized
        result.primary_track = track_mapping.get("primary_track")
        result.secondary_track = track_mapping.get("secondary_track")
        result.updated_at = datetime.utcnow()

    db.session.commit()

    # Step 5: return all computed data
    return {
        "normalized_scores": normalized,
        **track_mapping,
    }
