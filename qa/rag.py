from langchain_core.documents import Document
from qa.llm import ask_llm
from qa.vector_store import create_vector_store, retrieve_similar_chunks
import re


def build_documents(text):
    """
    Convert raw text into LangChain Document objects.
    """
    return [Document(page_content=text)]


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

    return [Document(page_content=c) for c in chunks]


def rag_pipeline(question, full_text):
    """
    Execute the complete RAG pipeline.
    """
    docs = semantic_split(full_text)                # 1. chunking
    vectorstore = create_vector_store(docs)        # 2. embedding + FAISS
    context = retrieve_similar_chunks(vectorstore, question)  # 3. retrieval
    answer = ask_llm(question, context)            # 4. LLM response
    return answer