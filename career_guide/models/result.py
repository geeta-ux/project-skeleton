from datetime import datetime
from career_guide import db

class Result(db.Model):
    __tablename__ = "results"

    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey("assessments.id", ondelete="CASCADE"))
    scores = db.Column(db.JSON)
    primary_track = db.Column(db.String(100))
    secondary_track = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Result assessment_id={self.assessment_id} primary={self.primary_track}>"
