from pymongo import MongoClient
from google.colab import userdata
from pymongo.operations import SearchIndexModel
from collections import defaultdict

MONGODB_URI = userdata.get("MONGODB_URI")
mongo_conn = MongoClient(MONGODB_URI)
MONGODB_DATABASE="synqanun"

db_client = mongo_conn[MONGODB_DATABASE]

collection = db_client["legal_chunks"]
def insert_many(full_chunks):
  collection.delete_many({})
  result = collection.insert_many(full_chunks)
  print("Inserted:", len(result.inserted_ids))

def create_search_index(collection):
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

def vector_search(query_vector,top_k,collection):
        

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

