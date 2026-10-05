from docx import Document
def parsing(doc_name):
    doc = Document(f"data/documents/fatwas/{doc_name}.docx")

    paragraphs = [
        p.text.strip()
        for p in doc.paragraphs
        if p.text.strip()
    ]

    metadata = doc_name
    header =paragraphs[0]
    content = ""
    opinion = ""

    for i, text in enumerate(paragraphs):

        if text.startswith("مبدأ"):
            content = paragraphs[i + 1]

        elif text == "الرأى":
            opinion = paragraphs[i + 1]
    sections = [
    {
        "source_file": doc_name,
        "section": "content",
        "text": content
    },
    {
        "source_file": doc_name,
        "section": "opinion",
        "text": opinion
    }
    ]
    print("Metadata:")
    print(metadata)

    print("\nHeader:")
    print(header)

    print("\nContent:")
    print(content)

    print("\nOpinion:")
    print(opinion)
    return sections