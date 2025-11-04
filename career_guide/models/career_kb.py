from career_guide import db

class CareerKB(db.Model):
    __tablename__ = "career_kb"

    id = db.Column(db.Integer, primary_key=True)
    career_id = db.Column(db.Integer, db.ForeignKey("careers.id", ondelete="CASCADE"), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tags = db.Column(db.ARRAY(db.String))  # PostgreSQL array for tags


    # Relationship back to the Career model
    career = db.relationship("Career", back_populates="knowledge_items")

    def __repr__(self):
        return f"<CareerKB {self.title} (Career ID: {self.career_id})>"
