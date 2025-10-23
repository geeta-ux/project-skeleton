def calculate_scores(responses):
    # Example scoring logic
    section_scores = {}
    for r in responses:
        section = r.assessment.responses[0].assessment_id  # you can tag question.section in future
        section_scores[section] = section_scores.get(section, 0) + (r.score or 1)

    total = sum(section_scores.values())
    primary = "Software Engineering" if total > 30 else "Marketing"
    secondary = "Data Analysis" if total > 20 else "Operations"
    return section_scores, primary, secondary
