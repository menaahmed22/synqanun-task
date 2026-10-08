
from fastapi import FastAPI, Query, HTTPException
from app.services.retriever import  retrive_chunks

app = FastAPI(
    title="SynQanun Semantic Search API",
    description="Semantic search over Arabic legal documents",
    version="1.0.0"
)


@app.get("/")
def root():
    return {"message": "SynQanun Semantic Search API is running"}


@app.get("/search")
def search(
    q: str = Query(..., min_length=3),
    top_k: int = Query(default=3, alias="topK", ge=1, le=10)
):
    try:
        # Retrieve matching chunks from MongoDB
        # chunks = search_chunks(q, limit=max(top_k * 5, 10))

        # Aggregate chunks into document-level results
        results = retrive_chunks(q, top_k=top_k)

        return {
            "query": q,
            "count": len(results),
            "results": results
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while searching legal documents."
        ) from exc