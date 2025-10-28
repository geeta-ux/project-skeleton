from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB
from .. import db

class Result(db.Model):
    __tablename__ = "results"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    assessment_id = db.Column(db.Integer, db.ForeignKey("assessments.id"))
    scores = db.Column(JSONB)  # ✅ switched to JSONB
    recommended_careers = db.Column(JSONB)  # ✅ switched to JSONB
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Result assessment_id={self.assessment_id} primary={self.primary_track}>"
