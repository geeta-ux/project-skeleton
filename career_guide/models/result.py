from career_guide import db
from datetime import datetime

class Result(db.Model):
    __tablename__ = "results"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
    assessment_id = db.Column(db.Integer, db.ForeignKey("assessments.id", ondelete="CASCADE"))
    scores = db.Column(db.JSON)  # Use scores_json here
    primary_track = db.Column(db.String(100))
    secondary_track = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    user = db.relationship("User", backref="results", lazy=True)
    assessment = db.relationship("Assessment", backref="results", lazy=True)
