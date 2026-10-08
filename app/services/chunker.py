from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import Settings
def chunk_sections(sections ,max_length=Settings.chunk_size ,chunk_overlap =Settings.chunk_overlap):
    chunks = []
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=max_length,
        chunk_overlap=chunk_overlap
    )

    for section in sections:
        text = section["text"]
        document_id = section["document_id"]
        document_type=section ["document_type"]
        sec_name = section["section"]

        if len(text) <= max_length:
            chunks.append({
                "document_id": document_id,
                "document_type": document_type,
                "section": sec_name,
                "chunk_id": f"{document_id}_{sec_name}_0",
                "text": text
            })
        else:
            split_texts = splitter.split_text(text)
            for i, chunk in enumerate(split_texts):
                chunks.append({
                    "document_id": document_id,
                    "document_type" :document_type,
                    "section": sec_name,
                    "chunk_id": f"{document_id}_{sec_name}_{i}",
                    "text": chunk
                })

    return chunks

