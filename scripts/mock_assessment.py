# career_guide/scripts/mock_assessment.py
from career_guide import create_app, db
from career_guide.models.user import User
from career_guide.models.assessment import Assessment
from career_guide.models.response import Response
from career_guide.models.result import Result

def insert_mock_assessment():
    print("🔹 Starting mock assessment insertion...")

    # Create app context
    app = create_app()
    with app.app_context():
        # Check if mock user already exists
        user = User.query.filter_by(email="mockuser@example.com").first()
        if not user:
            user = User(name="Mock User", email="mockuser@example.com")
            user.set_password("test123")
            db.session.add(user)
            db.session.commit()
            print("✅ Created mock user")

        # Create assessment
        assessment = Assessment(user_id=user.id, title="Mock Career Assessment")
        db.session.add(assessment)
        db.session.commit()
        print("✅ Created mock assessment")

        # Add responses
        response1 = Response(assessment_id=assessment.id, question_id=1, answer="Teamwork", score=3)
        response2 = Response(assessment_id=assessment.id, question_id=2, answer="Leadership", score=4)
        db.session.add_all([response1, response2])
        db.session.commit()
        print("✅ Added mock responses")

        # Add result
        result = Result(user_id=user.id, assessment_id=assessment.id, summary="Recommended Career: Project Manager")
        db.session.add(result)
        db.session.commit()
        print("✅ Added mock result")

        print("🎉 Mock data inserted successfully!")

if __name__ == "__main__":
    insert_mock_assessment()
