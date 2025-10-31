import pytest
from career_guide.services.scoring import calculate_scores
from career_guide.models import db, Result, User, Assessment

@pytest.fixture
def sample_assessment(app, client):
    # create test assessment & user in test DB
    a = Assessment(name="test", id=999)
    u = User(username="testuser", id=999)
    db.session.add_all([a, u])
    db.session.commit()
    yield {'assessment': a, 'user': u}
    # teardown
    db.session.delete(a); db.session.delete(u)
    db.session.commit()

def test_calculate_scores_returns_result_object(app, sample_assessment):
    u = sample_assessment['user'].id
    a = sample_assessment['assessment'].id
    # call calculate_scores — ensure it doesn't raise and returns a dict or saved Result
    out = calculate_scores(u, a)
    assert out is not None
    # if calculate_scores returns a Result instance, test attributes
    if hasattr(out, 'id'):
        assert out.user_id == u
        assert out.assessment_id == a
        assert isinstance(out.scores, dict)
