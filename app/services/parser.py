from docx import Document
from pathlib import Path

def parsing(file_path):
    doc = Document(file_path)
    path = Path(file_path)

    paragraphs = [
        p.text.strip()
        for p in doc.paragraphs
        if p.text.strip()
    ]

    document_id = path.stem
    document_type = path.parent.name

    # header =paragraphs[0]
    content = ""
    opinion = ""

    for i, text in enumerate(paragraphs):

        if text.startswith("مبدأ"):
            content = paragraphs[i + 1]

        elif text == "الرأى":
            opinion = paragraphs[i + 1]

        else :
          general =  paragraphs[i]  

    sections = [
    {
        "document_id": document_id,
        "document_type" : document_type,
        "section": "content",
        "text": content
    },
    {
        
        "document_id": document_id,
        "document_type" : document_type,
        "section": "opinion",
        "text": opinion
    },
    {     
        "document_id": document_id,
        "document_type" : document_type,
        "section": "general",
        "text": general
    }
    
    ]
  
    return sections