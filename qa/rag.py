import os
import re

# Django model for fetching text from DB
from documents.models import Document

# LangChain Document for vectorstore chunks
from langchain_core.documents import Document as LC_Document

from qa.llm import ask_llm
from qa.vector_store import create_vector_store, retrieve_similar_chunks


def build_documents(text):
    """
    Convert raw text into LangChain Document objects.
    """
    return [LC_Document(page_content=text)]


def semantic_split(text):
    """
    Split text into sentence-based semantic chunks.
    """
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = ""
    max_words = 120

    for sentence in sentences:
        if len(current_chunk.split()) + len(sentence.split()) <= max_words:
            current_chunk += " " + sentence
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    # Convert each chunk to LangChain Document for vectorstore
    return [LC_Document(page_content=c) for c in chunks]


def rag_pipeline(question):
    """
    Execute the complete RAG pipeline.
    """

    # Step 1: Load all documents from database
    all_docs = Document.objects.all()

    # Step 2: Split all documents into chunks
    chunks = []

    for doc in all_docs:
        chunks.extend(semantic_split(doc.content))

    if not chunks:
        return "No documents found in the database. Please upload a document first."

    # Step 3: Create vector store
    vectorstore = create_vector_store(chunks)

    # Step 4: Retrieve relevant chunks
    context = retrieve_similar_chunks(vectorstore, question)

    # Step 5: Generate answer using LLM
    return ask_llm(question, context)