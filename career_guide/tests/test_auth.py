import pytest
from career_guide import create_app, db
from career_guide.models.user import User

@pytest.fixture
def client():
    app = create_app("testing")
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_register_login_logout(client):
    # Register user
    resp = client.post("/auth/register", data={
        "name": "Test User",
        "email": "test@example.com",
        "password": "test123",
        "confirm": "test123"
    }, follow_redirects=True)
    assert b"success" in resp.data or resp.status_code == 200

    # Login
    resp = client.post("/auth/login", data={
        "email": "test@example.com",
        "password": "test123"
    }, follow_redirects=True)
    assert b"Logout" in resp.data

    # Logout
    resp = client.get("/auth/logout", follow_redirects=True)
    assert b"Login" in resp.data
