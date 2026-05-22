# Document Question Answering System (RAG-based AI Assistant)

## Project Description

This project is an AI-powered Document Question Answering System developed using Django, LangChain, and Retrieval-Augmented Generation (RAG). The system allows users to upload and manage DOCX documents, automatically extract and process their content, and ask natural language questions based on the uploaded documents.

To improve answer quality, the documents are semantically divided into smaller chunks and converted into vector embeddings, which are stored and searched using FAISS. When a question is submitted, the system retrieves the most relevant parts of the documents through semantic similarity search and provides a context-aware answer using a Large Language Model (LLM) connected through the OpenRouter API.

The entire workflow, including document management, question submission, and answer history tracking, is handled through the Django Admin panel.

## Key Features

- Upload and manage DOCX documents
- Automatic text extraction from uploaded files
- Semantic document chunking
- Vector-based similarity search using FAISS
- Retrieval-Augmented Generation (RAG) pipeline
- Natural language question answering with LLMs
- Question and answer history tracking
- Django Admin-based management interface
- API support for document management and question answering
- LangChain integration for LLM orchestration
