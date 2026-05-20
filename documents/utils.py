from docx import Document


def extract_text_from_docx(file_path):
    doc = Document(file_path)

    full_text = []

    for paragraph in doc.paragraphs:
        full_text.append(paragraph.text)

    return "\n".join(full_text)