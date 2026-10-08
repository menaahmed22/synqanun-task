from collections import defaultdict
from app.services.Mongodb import vector_search
from app.services.Mongodb import collection

def retrive_chunks(query, top_k=3,):
    results=vector_search(query,3,collection=collection)
    documents = defaultdict(list)

    for result in results:
        documents[result["document_id"]].append(result)

    document_results = []

    for document_id, document_chunks in documents.items():

        best_chunk = max(
            document_chunks,
            key=lambda x: x["score"]
        )

        document_results.append({
            "document_id": document_id,
            "document_type": best_chunk["document_type"],
            "score": best_chunk["score"],
            "best_chunk_id": best_chunk["chunk_id"],
            "section": best_chunk["section"],
            "snippet": best_chunk["text"]
        })

    document_results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return document_results[:top_k]