# career_guide/services/planning.py

def map_scores_to_tracks(scores: dict) -> dict:
    """
    Rule-based mapping from normalized section scores to career tracks.
    Returns: dict with primary_track, secondary_track, and all track_scores.
    """

    if not scores:
        return {"primary_track": None, "secondary_track": None, "track_scores": {}}

    # Define weighted importance of each section for every career track
    track_weights = {
        "Data": {
            "logical": 0.4,
            "numerical": 0.4,
            "verbal": 0.1,
            "creative": 0.05,
            "empathy": 0.05,
        },
        "Software": {
            "logical": 0.4,
            "numerical": 0.3,
            "verbal": 0.1,
            "creative": 0.1,
            "empathy": 0.1,
        },
        "Product": {
            "logical": 0.2,
            "numerical": 0.2,
            "verbal": 0.2,
            "creative": 0.2,
            "empathy": 0.2,
        },
        "Design": {
            "creative": 0.5,
            "verbal": 0.2,
            "logical": 0.1,
            "empathy": 0.2,
        },
        "Health-Informatics": {
            "empathy": 0.4,
            "verbal": 0.2,
            "logical": 0.2,
            "numerical": 0.2,
        },
    }

    # Compute weighted score for each track
    track_scores = {}
    for track, weights in track_weights.items():
        track_scores[track] = round(
            sum(scores.get(sec, 0) * w for sec, w in weights.items()), 3
        )

    # Sort tracks by score descending
    sorted_tracks = sorted(track_scores.items(), key=lambda x: x[1], reverse=True)
    primary = sorted_tracks[0][0]
    secondary = sorted_tracks[1][0]

    return {
        "primary_track": primary,
        "secondary_track": secondary,
        "track_scores": track_scores,
    }
