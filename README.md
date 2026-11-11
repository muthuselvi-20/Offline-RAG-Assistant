# Offline RAG Document Assistant

An AI-powered document assistant that allows users to upload PDF, DOCX, and image files and ask questions based on their content. It uses Retrieval-Augmented Generation (RAG), OCR, embeddings, and vector search to retrieve relevant information and generate context-aware answers using a locally running LLM.

## 🚀 Features

- **Multi-format Support:** Upload PDF, DOCX, and image files.
- **Text Extraction:** Extract text from documents using PyPDF, python-docx, and EasyOCR.
- **OCR Support:** Extract text from images using EasyOCR.
- **Text Chunking:** Split extracted content into smaller chunks for efficient retrieval.
- **Embeddings:** Convert text chunks into numerical vectors using Sentence Transformers.
- **Vector Database:** Store and retrieve document embeddings using ChromaDB.
- **RAG Pipeline:** Retrieve relevant document content and generate context-based answers.
- **Local LLM:** Generate responses using Ollama with Qwen3.
- **Chat History:** Maintain conversation history across sessions.

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Frontend | Streamlit |
| Backend | FastAPI |
| LLM | Ollama – Qwen3 |
| Embedding Model | Sentence Transformers |
| Vector Database | ChromaDB |
| PDF Processing | PyPDF |
| DOCX Processing | python-docx |
| Image Processing | OpenCV, EasyOCR |

## 📁 Project Structure

```text
Offline-Model/
│
├── main.py
├── llm.py
├── pdf_reader.py
├── doc_reader.py
├── ocr_reader.py
├── vectordb.py
├── history.py
│
├── app.py
│
├── uploads/
├── chroma_db/
├── chat_history/
│
├── pyproject.toml
├── uv.lock
└── README.md
```

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/muthuselvi-20/Offline-RAG-Assistant.git
```

```bash
cd Offline-Model
```

### 2. Install Dependencies

Install Python 3.11 or later.

Install uv:

```bash
pip install uv
```

Create the virtual environment and install project dependencies:

```bash
uv sync
```

### 3. Install Ollama

Download Ollama:

https://ollama.com/

Pull the Qwen3 model:

```bash
ollama pull qwen3:4b
```

Start Ollama:

```bash
ollama serve
```

### 4. Run the Application

Open another terminal in the project directory:

```bash
streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```

## 🔄 RAG Workflow

1. **Upload:** User uploads PDF, DOCX, or image files.
2. **Extraction:** Extract text from the uploaded documents.
3. **Chunking:** Divide extracted text into smaller chunks.
4. **Embedding:** Convert chunks into vector embeddings.
5. **Storage:** Store embeddings in ChromaDB.
6. **Retrieval:** Convert the user's question into an embedding and retrieve relevant chunks.
7. **Generation:** Send the retrieved context to Qwen3 through Ollama.
8. **Response:** Display the generated answer with relevant document references.

## 🧠 How RAG Works

Retrieval-Augmented Generation combines information retrieval with large language models.

Instead of relying only on the model's pre-trained knowledge, the application retrieves relevant information from uploaded documents and uses that information to generate answers.

## 🔒 Privacy

- Documents are processed locally.
- Embeddings are stored in a local ChromaDB database.
- The LLM runs locally through Ollama.
- No external LLM API is required.

## 🔮 Future Improvements

- Support additional document formats.
- Improve retrieval accuracy using hybrid search.
- Add document summarization.
- Support multilingual OCR.
- Add user authentication.
- Develop a web-based multi-user version.

## 👩‍💻 Author

**Muthuselvi A**

GitHub: https://github.com/muthuselvi-20

---

⭐ If you find this project useful, consider giving it a star!
