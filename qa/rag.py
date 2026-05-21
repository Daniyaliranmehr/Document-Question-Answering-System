import os
import re

# Django model for fetching text from DB
from documents.models import Document

# LangChain Document for vectorstore chunks
from langchain_core.documents import Document as LC_Document

from qa.llm import ask_llm
from qa.vector_store import create_vector_store, retrieve_similar_chunks, save_vector_store, load_vector_store


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


def rag_pipeline(question, index_path="faiss_index"):
    """
    Execute the complete RAG pipeline.
    - Automatically builds vectorstore if it does not exist.
    - Retrieves top-k relevant chunks using semantic similarity.
    - Returns LLM answer.
    """
    # Step 1: Load or create FAISS vectorstore
    if not os.path.exists(index_path):
        # Fetch all text from database (Django model)
        all_docs = Document.objects.all()
        chunks = []
        for doc in all_docs:
            chunks.extend(semantic_split(doc.content))
        vectorstore = create_vector_store(chunks)
        save_vector_store(vectorstore, path=index_path)
    else:
        vectorstore = load_vector_store(path=index_path)
    
    # Step 2: Semantic retrieval
    context = retrieve_similar_chunks(vectorstore, question)  # top-k chunks

    # Step 3: LLM answer
    return ask_llm(question, context)