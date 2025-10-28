from sqlalchemy.dialects.postgresql import JSONB
from .. import db

class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    section = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    options = db.Column(JSONB)  # ✅ switched to JSONB
    correct_answer = db.Column(db.String(255))
    weight = db.Column(db.Float, default=1.0)
