import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv("/content/synqanun-task/mena.env")


@dataclass(frozen=True)
class Settings:
    mongodb_uri: str = os.getenv("MONGODB_URI", "")
    mongodb_database: str = os.getenv("MONGODB_DATABASE", "synqanun")
    mongodb_collection: str = os.getenv("MONGODB_COLLECTION", "legal_chunks")
    mongodb_vector_index: str = os.getenv("MONGODB_VECTOR_INDEX", "legal_vector_index")

    embedding_model: str = os.getenv(
        "EMBEDDING_MODEL",
        "intfloat/multilingual-e5-base",
    )
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "1000"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "50"))
    search_index_dim :int = int(os.getenv("search_index_dim","768"))
    search_index_similarity :str =str(os.getenv("search_index_similarity","cosine"))





settings = Settings()