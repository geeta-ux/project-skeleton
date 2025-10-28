from career_guide import db

class Response(db.Model):
    __tablename__ = "responses"

    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey("assessments.id", ondelete="CASCADE"))
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id", ondelete="CASCADE"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    selected_option = db.Column(db.String(255))
    score = db.Column(db.Float, default=0.0)

    def __repr__(self):
        return f"<Response assess_id={self.assessment_id} q_id={self.question_id}>"
