from pymongo import MongoClient
from google.colab import userdata
from pymongo.operations import SearchIndexModel
from collections import defaultdict
from app.services.embedding import get_query_embedding

MONGODB_URI = userdata.get("MONGODB_URI")
mongo_conn = MongoClient(MONGODB_URI)
MONGODB_DATABASE="synqanun"
db_client = mongo_conn[MONGODB_DATABASE]

collection = db_client["legal_chunks"]
def insert_many(full_chunks):
  collection.delete_many({})
  result = collection.insert_many(full_chunks)
  print("Inserted:", len(result.inserted_ids))

def generate_vectors_index(collection):
    index_model = SearchIndexModel(
        definition={
            "mappings": {
                "dynamic": False,
                "fields": {
                    "embedding": {
                        "type": "knnVector",
                        "dimensions": 768,
                        "similarity": "cosine"
                    }
                }
            }
        },
        name="legal_vector_index"
    )
    collection.create_search_index(model=index_model)
    


def vector_search(query,top_k,collection):
        
    query_vector=get_query_embedding(query)

    client = mongo_conn

    collection = collection

    pipeline = [
        {
            "$vectorSearch": {
                "index": "legal_vector_index",
                "path": "embedding",
                "queryVector": query_vector,
                "numCandidates": max(top_k * 10, 20),
                "limit": max(top_k * 5, 10)
            }
        },
        {
            "$project": {
                # "_id": 1,
                "document_id": 1,
                'document_type': 1,
                'section' :1,
                "chunk_id": 1,
                "text": 1,
                "score": {
                    "$meta": "vectorSearchScore"
                },
            }
        },
    ]

    results = list(collection.aggregate(pipeline))

    # for result in results:
        # print("Document:", result.get("document_id"))
        # print("Year:", result.get("year"))
        # print("Score:", result.get("score"))
        # print("Text:", result.get("text"))
        # print("-" * 60)

    return results    

