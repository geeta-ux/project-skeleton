# career_guide/scripts/seed_milvus_kb.py
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility
from sentence_transformers import SentenceTransformer
from career_guide import create_app, db
from career_guide.models.career_kb import CareerKB

# Step 1. Connect to Flask + DB context
app = create_app()
app.app_context().push()

# Step 2. Connect to Milvus
connections.connect("default", host="localhost", port="19530")

collection_name = "career_kb"

# Step 3. Define schema (only once)
if not utility.has_collection(collection_name):
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=False),
        FieldSchema(name="career_id", dtype=DataType.INT64),
        FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=2000),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384),
    ]
    schema = CollectionSchema(fields=fields, description="Career Knowledge Base Embeddings")
    collection = Collection(name=collection_name, schema=schema)
    print("✅ Created new Milvus collection:", collection_name)
else:
    collection = Collection(collection_name)
    print("ℹ️ Collection already exists — inserting into it")

# Step 4. Load KB data from DB
items = CareerKB.query.all()
if not items:
    print("⚠️ No records found in career_kb table.")
    exit()

contents = [f"{item.title}. {item.content}" for item in items]
ids = [item.id for item in items]
career_ids = [item.career_id for item in items]

# Step 5. Generate embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(contents).tolist()

# Step 6. Insert into Milvus
collection.insert([ids, career_ids, contents, embeddings])
collection.flush()

print(f"✅ Inserted {len(items)} records into Milvus collection '{collection_name}'")
