from collections import defaultdict


documents = defaultdict(list)
def retrive_chunks(results,top_k):
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