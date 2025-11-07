from pymilvus import connections, Collection, utility, FieldSchema, CollectionSchema, DataType

class MilvusService:
    def __init__(self):
        # connect to Milvus (running in Docker)
        connections.connect("default", host="localhost", port="19530")

    def create_collection(self):
        collection_name = "career_kb"

        if not utility.has_collection(collection_name):
            fields = [
                FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
                FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384),
                FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=1000)
            ]
            schema = CollectionSchema(fields, description="Career knowledge base embeddings")
            collection = Collection(name=collection_name, schema=schema)
        else:
            collection = Collection(name=collection_name)

        return collection
