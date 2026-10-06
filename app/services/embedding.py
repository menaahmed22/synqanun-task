from sentence_transformers import SentenceTransformer
model = SentenceTransformer("intfloat/multilingual-e5-base")

def get_docs_embeddings(chunks):
  texts = [
    f"passage: {chunk['text']}"
    for chunk in chunks
  ]

  docs_embeddings = model.encode(
    texts,
    normalize_embeddings=True
  )
  
  return docs_embeddings

def get_query_embedding(query):
  query_embedding = model.encode(
        f"query: {query}",
        normalize_embeddings=True
    ).tolist()
  return query_embedding  
