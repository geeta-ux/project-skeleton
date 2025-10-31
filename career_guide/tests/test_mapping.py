import pytest
from career_guide.services import map_scores_to_careers

def test_mapping_outputs_list():
    # sample input: section scores
    sample_scores = {"section_a": 80, "section_b": 60}
    careers = map_scores_to_careers(sample_scores)
    assert isinstance(careers, list)
    # each item maybe tuple or dict depending on your implementation
    assert len(careers) >= 1
