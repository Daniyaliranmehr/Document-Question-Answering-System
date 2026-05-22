from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def create_vector_store(chunks):
    """
    Converts text chunks into embeddings for semantic search.
    """
    vectorstore = FAISS.from_documents(chunks, embedding_model)
    return vectorstore


def save_vector_store(vectorstore, path="faiss_index"):
    """
    Save FAISS vector database locally.
    """
    vectorstore.save_local(path)


def load_vector_store(path="faiss_index"):
    """
    Load FAISS vector database from local disk.
    """
    return FAISS.load_local(path, embedding_model, allow_dangerous_deserialization=True)


def retrieve_similar_chunks(vectorstore, question, k=3):
    """
    Retrieve top-k most relevant chunks using semantic similarity search.
    """
    docs = vectorstore.similarity_search(question, k=k)
    return "\n".join([doc.page_content for doc in docs])