from sqlalchemy import or_, func
from career_guide import db
from career_guide.models.career_kb import CareerKB
from career_guide.services.embedding import get_embedding
from pymilvus import Collection, connections, utility, CollectionSchema, FieldSchema, DataType

_milvus_connected = False
_milvus_collection = None
_COLLECTION_NAME = "career_kb"

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

def ensure_collection():
    """Ensure collection exists, insert schema if missing, create index if missing."""
    global _milvus_collection

    if not connect_milvus():
        return None

    if _milvus_collection:
        return _milvus_collection

    # Create collection if it doesn't exist
    if not utility.has_collection(_COLLECTION_NAME):
        print(f"⚙️ Collection '{_COLLECTION_NAME}' not found. Creating...")
        fields = [
            FieldSchema(name="kb_id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="title", dtype=DataType.VARCHAR, max_length=255),
            FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=2000),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384),
        ]
        schema = CollectionSchema(fields, description="Career Knowledge Base embeddings")
        _milvus_collection = Collection(name=_COLLECTION_NAME, schema=schema)
        print(f"✅ Created collection '{_COLLECTION_NAME}'")
    else:
        _milvus_collection = Collection(_COLLECTION_NAME)

    # Insert data if empty
    _milvus_collection.load()
    if _milvus_collection.num_entities == 0:
        print("⚠️ Collection is empty. Consider running init_and_load_kb.py to insert data.")

    # Create index if none exists
    if not _milvus_collection.indexes:
        print("⚙️ Creating index on 'embedding' field...")
        index_params = {
            "index_type": "IVF_FLAT",
            "metric_type": "COSINE",
            "params": {"nlist": 128},
        }
        _milvus_collection.create_index(field_name="embedding", index_params=index_params)
        print("✅ Index created")

    # Load collection
    _milvus_collection.load()
    print(f"✅ Collection '{_COLLECTION_NAME}' loaded with {_milvus_collection.num_entities} entities")
    return _milvus_collection

def semantic_search(query_vector, top_k=5):
    col = ensure_collection()
    if not col or col.num_entities == 0:
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
        if query_vector:
            results = semantic_search(query_vector, top_k)
            if results:
                return results

        # Fallback: keyword search in PostgreSQL
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
        return [
            {
                "title": r.title,
                "content": r.content
            }
            for r in results
        ]

    except Exception as e:
        print("❌ Error in retrieve_career_kb:", e)
        return []
