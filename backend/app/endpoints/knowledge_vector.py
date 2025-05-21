from fastapi import APIRouter, UploadFile, Form
from app.utils.chunker import chunk_text
from app.core.knowledge_vector import add_knowledge_chunks
from app.core.knowledge_vector import collection

router = APIRouter()

@router.post("/upload/")
async def upload_knowledge(topic: str = Form(...), file: UploadFile = Form(...)):
    """
    Uploads a text file and stores its content in the vector database as knowledge chunks.

    The file is split into smaller chunks using a text chunking utility,
    and each chunk is stored with the associated topic for semantic search.

    Args:
        topic (str): A label or category for the uploaded content.
        file (UploadFile): A plain text file (.txt) containing the knowledge content.

    Returns:
        dict: Upload status and the number of chunks created.
    """
    content = (await file.read()).decode("utf-8")
    chunks = chunk_text(content)
    add_knowledge_chunks(topic, chunks)
    return {"status": "uploaded", "chunks": len(chunks)}


@router.get("/list")
def list_chunks():
    """
    Retrieves all stored knowledge chunks and their associated metadata from the vector database.

    Returns:
        list[dict]: A list of stored documents and their metadata.
    """
    return collection.get(include=["documents", "metadatas"])