from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from qa.llm import ask_llm


def build_documents(text):
    """
    Convert raw text into LangChain Document objects.
    """
    return [Document(page_content=text)]


def split_documents(docs):
    """
    Split documents into smaller text chunks.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    return splitter.split_documents(docs)


def retrieve_context(chunks, question):
    """
    Retrieve the most relevant chunk using simple keyword matching.
    """
    best_chunk = ""

    for chunk in chunks:
        if question.lower() in chunk.page_content.lower():
            best_chunk = chunk.page_content
            break

    if not best_chunk and chunks:
        best_chunk = chunks[0].page_content

    return best_chunk


def rag_pipeline(question, full_text):
    """
    Execute the complete RAG pipeline.
    """

    docs = build_documents(full_text)  # raw text → LangChain documents
    chunks = split_documents(docs)  # documents → chunks
    context = retrieve_context(chunks, question)  # find the best chunk

    answer = ask_llm(question, context)

    return answer