from .. import db

class Career(db.Model):
    __tablename__ = "careers"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    track = db.Column(db.String(100))
    skills = db.Column(db.JSON)
    description = db.Column(db.Text)
    avg_salary_range = db.Column(db.String(100))
    sample_roles = db.Column(db.JSON)