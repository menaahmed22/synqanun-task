from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_sections(sections):
    chunks = []
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )

    for section in sections:
        text = section["text"]
        source_file = section["source_file"]
        sec_name = section["section"]

        if len(text) <= 1000:
            chunks.append({
                "source_file": source_file,
                "section": sec_name,
                "chunk_id": f"{source_file}_{sec_name}_0",
                "text": text
            })
        else:
            split_texts = splitter.split_text(text)
            for i, chunk in enumerate(split_texts):
                chunks.append({
                    "source_file": source_file,
                    "section": sec_name,
                    "chunk_id": f"{source_file}_{sec_name}_{i}",
                    "text": chunk
                })

    return chunks

