# RAG Document Assistant

An offline document question-answering system.

## Features

- PDF upload
- DOCX upload
- TXT upload
- Image OCR
- Text chunking
- Embedding generation
- ChromaDB vector storage
- Semantic search
- LLM answer generation

## Technologies

- Python
- Streamlit
- LangChain Text Splitter
- Ollama
- ChromaDB
- EasyOCR

## Models

LLM: qwen3:4b

Embedding: nomic-embed-text

## Installation

Install dependencies:

pip install -r requirements.txt

Download models:

ollama pull qwen3:4b

ollama pull nomic-embed-text

## Run

streamlit run app.py