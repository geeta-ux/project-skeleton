# career_guide/services/skill_gap.py
from career_guide.models.career import Career

# 1️⃣ Expected skill profiles (target competency by domain)
skill_targets = {
    "logical": 0.8,
    "numerical": 0.8,
    "verbal": 0.7,
    "creative": 0.7,
    "empathy": 0.7,
}

# 2️⃣ Learning resources / actions per domain
learning_actions = {
    "logical": [
        "Practice daily logic puzzles (e.g., Brilliant.org, LeetCode Logic)",
        "Take an online Data Structures & Algorithms course",
    ],
    "numerical": [
        "Revise core math & statistics fundamentals",
        "Complete a 'Data Analysis with Python' or Excel course",
    ],
    "verbal": [
        "Join a public speaking or storytelling workshop",
        "Read and summarize one article per day",
    ],
    "creative": [
        "Explore UX design challenges on Dribbble or Figma",
        "Experiment with visual or writing projects weekly",
    ],
    "empathy": [
        "Take an active listening or leadership communication module",
        "Volunteer for mentoring or customer-support programs",
    ],
}

# 3️⃣ Map skill names → domains (simple keyword matching)
def infer_domain_from_skill(skill_name):
    s = skill_name.lower()
    if any(k in s for k in ["python", "sql", "data", "analytics", "logic"]):
        return "logical"
    if any(k in s for k in ["math", "quant", "number", "stat"]):
        return "numerical"
    if any(k in s for k in ["communication", "writing", "language", "verbal"]):
        return "verbal"
    if any(k in s for k in ["design", "ux", "creative", "innovation"]):
        return "creative"
    if any(k in s for k in ["empathy", "care", "team", "collaborate"]):
        return "empathy"
    return None

# 4️⃣ Generate Gap → Action list
def analyze_skill_gaps(career_title, user_scores):
    ideal_profiles = {
        "Data Scientist": {"logical": 0.85, "numerical": 0.9, "verbal": 0.6, "creative": 0.5, "empathy": 0.4},
        "UX Designer": {"creative": 0.9, "verbal": 0.7, "empathy": 0.8},
        "Software Engineer": {"logical": 0.8, "numerical": 0.75, "verbal": 0.5},
        "Healthcare Analyst": {"empathy": 0.8, "logical": 0.6, "numerical": 0.5},
    }

    learning_resources = {
        "logical": ["Practice algorithmic thinking", "Take logic puzzle courses"],
        "numerical": ["Work on data interpretation problems", "Study basic statistics"],
        "verbal": ["Improve technical writing and comprehension", "Read and summarize research papers"],
        "creative": ["Join design-thinking workshops", "Try brainstorming challenges"],
        "empathy": ["Learn user psychology", "Engage in team-based activities"]
    }

    target = ideal_profiles.get(career_title)
    if not target:
        return []  # 🟡 This causes your current empty output

    results = []
    for skill, required in target.items():
        current = user_scores.get(skill, 0)
        gap = round(required - current, 2)
        if gap > 0:
            results.append({
                "skill": skill.capitalize(),
                "domain": career_title,
                "gap": gap,
                "recommendations": learning_resources.get(skill, ["Explore this skill further."])
            })
    return results

