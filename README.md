# Arabic Legal Semantic Search

A semantic search system for Arabic legal documents using multilingual embeddings and MongoDB Atlas Vector Search.

## 1. Overview

The system retrieves relevant Arabic legal documents based on **meaning**, rather than exact keyword matching.

The search pipeline is:

```text
Legal Documents
      ↓
Parse Documents
      ↓
Chunk Text
      ↓
Generate Embeddings
      ↓
Store in MongoDB Atlas
      ↓
Vector Search
      ↓
Aggregate Chunks by Document
      ↓
Rank Documents
```

## 2. Chunking Strategy

Documents are first divided into available logical sections such as `content`, `opinion`, and `general`.

Long sections are then split using `RecursiveCharacterTextSplitter` with:

* Chunk size: **1000 characters**
* Chunk overlap: **50 characters**

The overlap helps preserve context between adjacent chunks.

Each chunk keeps metadata that identifies its original document, including:

* `document_id`
* `document_type`
* `section`
* `chunk_id`

This allows retrieved chunks to be mapped back to their source document.

## 3. Embeddings

The project uses:

```text
intfloat/multilingual-e5-base
```

This model supports multilingual text, including Arabic.


Embeddings are normalized and compared using **cosine similarity**.

## 4. Vector Storage

Vectors are stored in **MongoDB Atlas** using MongoDB Atlas Vector Search.

The vector field is:

```text
embedding
```

The vector index uses:

* Dimensions: **768**
* Similarity: **Cosine**

## 5. Retrieval

For each search query:

1. The query is converted into an embedding.
2. MongoDB Atlas Vector Search retrieves the most similar chunks.
3. Retrieved chunks are grouped by `document_id`.
4. The best matching chunk score is used as the document relevance score.
5. Documents are ranked by relevance.
6. The requested number of documents (`topK`) is returned.

More chunks than the requested document-level `topK` can be retrieved initially because multiple matching chunks may belong to the same document.

## 6. API

The application exposes a FastAPI endpoint:

```text
GET /search
```

Parameters:

```text
q      - Search query
topK   - Number of documents to return
```

Example:

<img width="1299" height="616" alt="image" src="https://github.com/user-attachments/assets/717a7982-ec68-4c9c-8af8-37bfb4fefe6b" />


## 7. Project Structure

```text
synqanun-task/
│
├── app/
│   ├── main.py
│   ├── config.py
│   └── services/
│       ├── chunker.py
│       ├── embedding.py
│       ├── parser.py
│       ├── Mongodb.py
│       ├── preparedocs.py
│       └── retriever.py
│
├── data/
│   └── documents/
│
├── example.env
├── requirements.txt
└── README.md
```

## 8. Limitations

* Retrieval quality depends on the embedding model and chunking strategy.
* The current system uses semantic similarity without a separate keyword retrieval stage.
* Document ranking is based on the best matching chunk.
* The system is designed for semantic search only and does not provide legal interpretation.

## 9. Running the Project

Install the dependencies:

```bash
pip install -r requirements.txt
```

Configure the MongoDB connection and required environment variables.

Run the FastAPI application:

```bash
uvicorn app.main:app --reload
```

The API can then be accessed through the FastAPI server.
