# scripts/sync_kb_to_milvus.py
from career_guide import create_app, db
from career_guide.models.career_kb import CareerKB
from career_guide.services.retrieve import upsert_kb_embedding

app = create_app()

with app.app_context():
    items = CareerKB.query.all()
    for kb in items:
        print(f"Embedding: {kb.title}")
        upsert_kb_embedding(kb.id, kb.career_id, kb.title, kb.content, kb.tags)
    print("✅ Sync complete.")
