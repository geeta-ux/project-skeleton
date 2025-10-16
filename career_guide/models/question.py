from .. import db

class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    section = db.Column(db.String(100))
    difficulty = db.Column(db.String(50))
    text = db.Column(db.Text, nullable=False)
    options = db.Column(db.JSON, nullable=False)
    correct_option = db.Column(db.String(255))
    weight = db.Column(db.Float, default=1.0)
