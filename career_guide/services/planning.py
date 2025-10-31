# career_guide/services/planning.py

def map_scores_to_tracks(scores: dict) -> dict:
    """
    Map normalized section scores to career tracks using weighted logic.
    Returns: dict with primary_track, secondary_track, and all track_scores.
    """

    if not scores:
        return {"primary_track": None, "secondary_track": None, "track_scores": {}}

    # ✅ Soft floor to prevent collapse (missing scores get neutral weight)
    for key, val in scores.items():
        if val == 0:
            scores[key] = 0.4

    # ✅ Define weighted importance of each section for every career track
    track_weights = {
        "Data": {
            "logical": 0.5,
            "numerical": 0.4,
            "verbal": 0.05,
            "creative": 0.03,
            "empathy": 0.02,
        },
        "Software": {
            "logical": 0.5,
            "numerical": 0.2,
            "verbal": 0.15,
            "creative": 0.1,
            "empathy": 0.05,
        },
        "Product": {
            "logical": 0.25,
            "numerical": 0.15,
            "verbal": 0.2,
            "creative": 0.2,
            "empathy": 0.2,
        },
        "Design": {
            "creative": 0.5,
            "verbal": 0.25,
            "logical": 0.05,
            "empathy": 0.2,
        },
        "Health-Informatics": {
            "logical": 0.3,
            "numerical": 0.1,
            "verbal": 0.1,
            "empathy": 0.5,
        },
    }

    # ✅ Compute weighted score for each track
    track_scores = {}
    for track, weights in track_weights.items():
        total = 0.0
        for sec, weight in weights.items():
            try:
                val = float(scores.get(sec, 0))
            except (TypeError, ValueError):
                val = 0.0
            total += val * weight
        track_scores[track] = round(total, 3)

    # ✅ Sort tracks safely
    sorted_tracks = sorted(track_scores.items(), key=lambda x: x[1], reverse=True)
    primary = sorted_tracks[0][0] if sorted_tracks else None
    secondary = sorted_tracks[1][0] if len(sorted_tracks) > 1 else None

    # ✅ Debugging info (optional)
    print(f"[DEBUG] TRACK SCORES: {track_scores}")
    print(f"[DEBUG] PRIMARY: {primary}, SECONDARY: {secondary}")

    return {
        "primary_track": primary,
        "secondary_track": secondary,
        "track_scores": track_scores,
    }

def generate_5year_plan(primary_track: str, chosen_career: str, scores: dict):
    """
    Generate a structured 5-year personalized career plan.
    Uses track + career + strengths to customize milestones.
    """
    base_plan = {
        "Year 1": [],
        "Year 2": [],
        "Year 3": [],
        "Year 4": [],
        "Year 5": []
    }

    # --- Common foundation (applies to all tracks)
    base_plan["Year 1"].extend([
        "Master foundations in core subjects relevant to your track",
        "Earn 1-2 certifications (e.g., Coursera, edX, Google, AWS)",
        "Build a small personal project to apply learning"
    ])

    base_plan["Year 2"].extend([
        "Work on intermediate-level projects",
        "Start publishing learnings (blog, GitHub, LinkedIn)",
        "Participate in hackathons or competitions"
    ])

    # --- Track-specific direction
    if primary_track == "Data":
        base_plan["Year 3"].extend([
            "Pursue internship or freelance work in data analytics or ML",
            "Learn advanced Python, SQL, and visualization tools",
            "Start contributing to open data projects"
        ])
        base_plan["Year 4"].extend([
            "Specialize in ML, AI, or Data Engineering",
            "Complete an industry-recognized certification (AWS Data, TensorFlow, etc.)"
        ])
        base_plan["Year 5"].extend([
            "Lead a data-driven product initiative or team",
            "Present at conferences or publish data case studies"
        ])

    elif primary_track == "Software":
        base_plan["Year 3"].extend([
            "Contribute to open-source repositories",
            "Explore system design, DevOps, or backend architecture"
        ])
        base_plan["Year 4"].extend([
            "Specialize in a domain (AI, Fullstack, Cloud, Mobile)",
            "Mentor juniors or peers"
        ])
        base_plan["Year 5"].extend([
            "Move into a lead engineer or architect role",
            "Build a high-impact product or startup prototype"
        ])

    elif primary_track == "Product":
        base_plan["Year 3"].extend([
            "Get internship or project experience in product or marketing",
            "Develop communication, storytelling, and research skills"
        ])
        base_plan["Year 4"].extend([
            "Lead cross-functional project teams",
            "Earn a certification like 'Product Management by Google'"
        ])
        base_plan["Year 5"].extend([
            "Move into product manager or strategy role",
            "Publish product case studies or launch your own product"
        ])

    elif primary_track == "Design":
        base_plan["Year 3"].extend([
            "Intern with UX/UI or visual design teams",
            "Build a strong design portfolio (Dribbble, Behance)"
        ])
        base_plan["Year 4"].extend([
            "Explore motion design or UX research",
            "Collaborate with developers to ship real-world designs"
        ])
        base_plan["Year 5"].extend([
            "Lead a creative design project",
            "Mentor upcoming designers"
        ])

    elif primary_track == "Health-Informatics":
        base_plan["Year 3"].extend([
            "Pursue internship in healthcare analytics or digital health",
            "Learn data privacy and compliance frameworks"
        ])
        base_plan["Year 4"].extend([
            "Specialize in predictive health analytics or telemedicine tech",
            "Collaborate with research labs"
        ])
        base_plan["Year 5"].extend([
            "Lead digital health innovation projects",
            "Publish a healthcare AI or informatics paper"
        ])

    # --- Personalization based on strong skills
    if scores.get("logical", 0) > 0.7:
        base_plan["Year 2"].append("Engage in analytical competitions like Kaggle or ICPC")
    if scores.get("creative", 0) > 0.7:
        base_plan["Year 3"].append("Design and publish a creative side project or app")
    if scores.get("empathy", 0) > 0.7:
        base_plan["Year 4"].append("Lead a peer-mentorship or community impact program")

    return base_plan

