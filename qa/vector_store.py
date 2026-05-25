from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def create_vector_store(chunks):
    """
    Converts text chunks into embeddings for semantic search.
    """
    vectorstore = FAISS.from_documents(chunks, embedding_model)
    return vectorstore


def retrieve_similar_chunks(vectorstore, question, k=3):
    """
    Retrieve top-k most relevant chunks using semantic similarity search.
    """
    docs = vectorstore.similarity_search(question, k=k)
    return "\n".join([doc.page_content for doc in docs])