from career_guide.models.career import Career
import math

def get_top_careers(primary_track: str, normalized_scores: dict, limit=3):
    # Get careers with matching track
    q = Career.query.filter_by(track=primary_track).all()
    results = []
    for c in q:
        skills = c.skills or []   # assuming JSON list stored
        # Score = number of matched skills * weighted factor from normalized_scores
        # Example simple heuristic: higher 'verbal' improves Product/Design matches
        skill_score = 0
        for s in skills:
            # map skill keywords to sections (light heuristic)
            if s.lower() in ("python","sql","machine learning","analytical thinking"):
                skill_score += normalized_scores.get("logical", 0) + normalized_scores.get("numerical", 0)
            elif s.lower() in ("communication","user research","empathy"):
                skill_score += normalized_scores.get("verbal", 0) + normalized_scores.get("empathy", 0)
            elif s.lower() in ("creativity","visual design","prototyping"):
                skill_score += normalized_scores.get("creative", 0)
            else:
                skill_score += 0.1
        results.append((c, round(skill_score, 3)))
    results.sort(key=lambda x: x[1], reverse=True)
    return [{"career": r[0], "score": r[1]} for r in results[:limit]]
