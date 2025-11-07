# career_guide/services/retrieve.py
from sqlalchemy import or_
from career_guide import db
from career_guide.models.career_kb import CareerKB

def retrieve_career_kb(query, top_k=5):
    """
    Retrieve top-K relevant career knowledge base entries.
    """
    try:
        # Simple keyword search (mock semantic)
        results = (
            db.session.query(CareerKB)
            .filter(
                or_(
                    CareerKB.title.ilike(f"%{query}%"),
                    CareerKB.content.ilike(f"%{query}%"),
                    CareerKB.tags.any(query.lower())
                )
            )
            .limit(top_k)
            .all()
        )

        # Convert to JSON-friendly dicts
        return [
            {
                "title": r.title,
                "content": r.content,
                "tags": r.tags,
                "career_id": r.career_id,
            }
            for r in results
        ]
    except Exception as e:
        print("❌ Error in retrieve_career_kb:", e)
        return []
