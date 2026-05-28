from docx import Document
import os
from PyPDF2 import PdfReader


def extract_text_from_docx(file_path):
    doc = Document(file_path)

    full_text = []

    for paragraph in doc.paragraphs:
        full_text.append(paragraph.text)

    return "\n".join(full_text)


def extract_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted + "\n"

    return text


def extract_text(file_path):
    extension = os.path.splitext(file_path)[1].lower()

    if extension == '.docx':
        return extract_text_from_docx(file_path)

    elif extension == '.txt':
        return extract_text_from_txt(file_path)
    
    elif extension == '.pdf':
        return extract_text_from_pdf(file_path)

    else:
        raise ValueError("Unsupported file format")