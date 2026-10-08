from app.services.parser import parsing
from app.services.chunker import chunk_sections
from app.services.embedding import get_docs_embeddings
from app.services.Mongodb import insert_many
from app.services.Mongodb import collection
from app.services.Mongodb import generate_vectors_index
def prepare_docs(file_path):
  sections = parsing(file_path)
  chunks=chunk_sections(sections)
  docs_embedding=get_docs_embeddings(chunks)
  for chunk, embedding in zip(chunks, docs_embedding):
    chunk["embedding"] = embedding.tolist()
  insert_database = insert_many(chunks) 
  for index in collection.list_search_indexes():
    print(index)
  generate_vectors_index(collection)
  


  

