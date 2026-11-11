import uuid

from pathlib import Path

from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException
)

from pydantic import BaseModel

from pdf_reader import read_pdf
from doc_reader import read_docx
from ocr_reader import read_image

from vectordb import (
    add_documents,
    get_total_chunks
)

from llm import generate_answer

from history import (
    create_session,
    save_message,
    get_history
)


# INITIALIZE FASTAPI

app = FastAPI(
    title="Offline RAG Document Assistant",
    description="Document question answering using RAG and Ollama",
    version="1.0.0"
)


UPLOAD_DIR = Path("uploads")

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# SUPPORTED FILES

SUPPORTED_EXTENSIONS = [
    ".pdf",
    ".docx",
    ".png",
    ".jpg",
    ".jpeg",
    ".bmp",
    ".tiff",
    ".webp"
]


# DOCUMENT PROCESSING

def process_file_bytes(
    filename,
    file_bytes
):

    extension = Path(filename).suffix.lower()

    if extension == ".pdf":

        documents = read_pdf(file_bytes)

    elif extension == ".docx":

        documents = read_docx(file_bytes)

    elif extension in [
        ".png",
        ".jpg",
        ".jpeg",
        ".bmp",
        ".tiff",
        ".webp"
    ]:

        documents = read_image(file_bytes)

    else:

        raise ValueError(
            "Unsupported file format"
        )

    if not documents:

        raise ValueError(
            "No readable text found in this file. "
            "For scanned PDFs, add a PDF OCR fallback."
        )

    # Generate unique file ID
    file_id = str(uuid.uuid4())

    # Save uploaded file
    safe_filename = Path(filename).name

    saved_path = (
        UPLOAD_DIR /
        f"{file_id}_{safe_filename}"
    )

    saved_path.write_bytes(
        file_bytes
    )

    # Store chunks in ChromaDB
    total_chunks = add_documents(

        documents=documents,

        source=safe_filename,

        file_id=file_id

    )

    return {

        "message": "Document processed successfully",

        "filename": safe_filename,

        "file_id": file_id,

        "chunks": total_chunks

    }


# QUESTION ANSWERING

def ask_question(
    question,
    session_id
):

    chat_history = get_history(
        session_id
    )

    result = generate_answer(

        question=question,

        chat_history=chat_history

    )

    save_message(

        session_id,

        "user",

        question

    )

    save_message(

        session_id,

        "assistant",

        result["answer"]

    )

    return result


# REQUEST MODEL

class QuestionRequest(BaseModel):

    question: str

    session_id: str | None = None


# HEALTH CHECK

@app.get("/health")
def health_check():

    return {

        "status": "running",

        "stored_chunks": get_total_chunks()

    }


# CREATE CHAT SESSION

@app.post("/session")
def new_session():

    session_id = create_session()

    return {

        "session_id": session_id

    }


# UPLOAD DOCUMENT

@app.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    filename = Path(file.filename or "").name

    extension = Path(filename).suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:

        raise HTTPException(

            status_code=400,

            detail="Unsupported file format"

        )

    try:

        file_bytes = await file.read()

        if not file_bytes:

            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty"
            )

        result = process_file_bytes(

            filename,

            file_bytes

        )

        return result

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# ASK QUESTION

@app.post("/ask")
def ask(request: QuestionRequest):

    if not request.question.strip():

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    session_id = (
        request.session_id or create_session()
    )

    try:

        result = ask_question(

            request.question.strip(),

            session_id

        )

        return {

            "session_id": session_id,

            "question": request.question,

            "answer": result["answer"],

            "sources": result["sources"]

        }

    except Exception as error:

        raise HTTPException(

            status_code=500,

            detail=str(error)

        )