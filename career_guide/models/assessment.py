# models/assessment.py
from datetime import datetime
from career_guide import db

class Assessment(db.Model):
    __tablename__ = "assessments"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)

    # responses = db.relationship(
    #     "Response", back_populates="assessment", cascade="all, delete-orphan"
    # )

    def __repr__(self):
        return f"<Assessment id={self.id} user_id={self.user_id}>"
