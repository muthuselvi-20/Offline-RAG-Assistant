import chromadb
import uuid

from sentence_transformers import SentenceTransformer


# Initialize embedding model
embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# Initialize persistent ChromaDB
client = chromadb.PersistentClient(
    path="./chroma_db"
)


collection = client.get_or_create_collection(
    name="document_collection",
    metadata={
        "hnsw:space": "cosine"
    }
)


# TEXT CHUNKING
def chunk_text(
    text,
    chunk_size=800,
    overlap=150
):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:

            chunks.append(chunk)

        if end >= len(text):

            break

        start = end - overlap

    return chunks


# CREATE EMBEDDINGS
def create_embeddings(texts):

    embeddings = embedding_model.encode(
        texts,
        convert_to_numpy=True
    )

    return embeddings.tolist()


# STORE DOCUMENTS
def add_documents(
    documents,
    source,
    file_id
):

    all_chunks = []

    all_metadata = []

    for document in documents:

        text = document["text"]

        page = document.get("page")

        chunks = chunk_text(text)

        for index, chunk in enumerate(chunks):

            all_chunks.append(chunk)

            all_metadata.append({

                "source": source,

                "file_id": file_id,

                "page": page if page is not None else -1,

                "chunk_index": index

            })

    if not all_chunks:

        return 0

    embeddings = create_embeddings(
        all_chunks
    )

    ids = [
        str(uuid.uuid4())
        for _ in all_chunks
    ]

    collection.add(

        ids=ids,

        documents=all_chunks,

        embeddings=embeddings,

        metadatas=all_metadata

    )

    return len(all_chunks)


# RETRIEVE RELEVANT DOCUMENTS
def search_documents(
    question,
    top_k=4
):

    if collection.count() == 0:

        return []

    query_embedding = create_embeddings(
        [question]
    )[0]

    results = collection.query(

        query_embeddings=[
            query_embedding
        ],

        n_results=min(
            top_k,
            collection.count()
        ),

        include=[
            "documents",
            "metadatas",
            "distances"
        ]

    )

    retrieved_documents = []

    for index, text in enumerate(
        results["documents"][0]
    ):

        metadata = results["metadatas"][0][index]

        distance = results["distances"][0][index]

        retrieved_documents.append({

            "text": text,

            "metadata": metadata,

            "distance": distance

        })

    return retrieved_documents


# TOTAL STORED CHUNKS
def get_total_chunks():

    return collection.count()


# DELETE DOCUMENT
def delete_document(file_id):

    collection.delete(

        where={
            "file_id": file_id
        }

    )