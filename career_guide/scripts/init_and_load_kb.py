# career_guide/services/retrieve.py
from sqlalchemy import or_, func
from career_guide import db
from career_guide.models.career_kb import CareerKB
from career_guide.services.embedding import get_embedding
from pymilvus import Collection, connections, utility
import importlib

_milvus_connected = False
_milvus_collection = None
COLLECTION_NAME = "career_kb"
VECTOR_DIM = 384

def connect_milvus():
    global _milvus_connected
    if _milvus_connected:
        return True
    try:
        connections.connect(alias="default", host="localhost", port="19530")
        _milvus_connected = True
        return True
    except Exception as e:
        print("⚠️ Milvus connection failed:", e)
        return False

def load_collection():
    """
    Load Milvus collection. If collection doesn't exist, auto-run init_and_load_kb.py
    """
    global _milvus_collection
    if _milvus_collection:
        return _milvus_collection

    if not connect_milvus():
        return None

    try:
        if not utility.has_collection(COLLECTION_NAME):
            print(f"⚠️ Collection '{COLLECTION_NAME}' not found. Initializing...")
            # Dynamically import and run init_and_load_kb.py
            init_script = importlib.import_module("career_guide.scripts.init_and_load_kb")
            # Reload module to ensure it runs if already imported
            importlib.reload(init_script)
            print("✅ Milvus collection initialized via init_and_load_kb.py")

        col = Collection(COLLECTION_NAME)
        col.load()
        print(f"✅ Collection '{COLLECTION_NAME}' loaded with {col.num_entities} entities")
        _milvus_collection = col
        return col

    except Exception as e:
        print(f"⚠️ Milvus collection load failed: {e}")
        return None

def semantic_search(query_vector, top_k=5):
    col = load_collection()
    if not col:
        return []

    try:
        search_params = {"metric_type": "COSINE", "params": {"nprobe": 10}}
        results = col.search(
            data=[query_vector],
            anns_field="embedding",
            param=search_params,
            limit=top_k,
            output_fields=["title", "content"]
        )

        kb_items = []
        for hit in results[0]:
            entity = hit.entity
            kb_items.append({
                "title": entity.get("title"),
                "content": entity.get("content")
            })
        return kb_items

    except Exception as e:
        print("⚠️ Milvus search failed:", e)
        return []

def retrieve_career_kb(query, top_k=5):
    """
    Hybrid retrieval: semantic search first, keyword search fallback
    """
    try:
        query_vector = get_embedding(query)
        results = []

        # Step 1: Semantic search
        if query_vector:
            results = semantic_search(query_vector, top_k)
            if results:
                return results  # return if semantic search succeeded

        # Step 2: Keyword search fallback
        print("⚠️ Falling back to keyword search...")
        results = (
            db.session.query(CareerKB)
            .filter(
                or_(
                    CareerKB.title.ilike(f"%{query}%"),
                    CareerKB.content.ilike(f"%{query}%"),
                    func.lower(func.array_to_string(CareerKB.tags, ',')).ilike(f"%{query.lower()}%")
                )
            )
            .limit(top_k)
            .all()
        )

        return [{"title": r.title or "", "content": r.content or ""} for r in results]

    except Exception as e:
        print("❌ Error in retrieve_career_kb:", e)
        return []
