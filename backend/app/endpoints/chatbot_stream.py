import os
import openai
from app.core.chatbot_engine import get_streaming_response, get_web_response, get_response_with_file
from fastapi import APIRouter, Request, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from uuid import uuid4
from app.db.database import db_session
from app.db.models import Conversation
from app.core.chatbot_engine import upload_and_store_file

router = APIRouter()

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/chatbot/stream")
async def stream_response(request: Request, convo_id: str, message: str):
    """
    Streams a chatbot response using OpenAI API and knowledge base vector search.

    Args:
        request (Request): The incoming HTTP request.
        convo_id (str): The conversation ID.
        message (str): The user’s input message.

    Returns:
        StreamingResponse: SSE stream with the assistant’s reply.
    """
    return StreamingResponse(
        get_streaming_response(convo_id, message),
        media_type="text/event-stream"
    )

@router.get("/chatbot/web")
async def stream_web_response(request: Request, convo_id: str, message: str):
    """
    Streams a chatbot response using OpenAI with web search capabilities.

    Args:
        request (Request): The incoming HTTP request.
        convo_id (str): The conversation ID.
        message (str): The user’s input message.

    Returns:
        StreamingResponse: SSE stream with a GPT-4-generated reply using web data.
    """
    return StreamingResponse(
        get_web_response(convo_id, message),
        media_type="text/event-stream"
    )

@router.get("/chatbot/file")
async def stream_file_response(request: Request, convo_id: str, message: str):
    """
    Streams a chatbot response using OpenAI API with file-based retrieval.

    Args:
        request (Request): The incoming HTTP request.
        convo_id (str): The conversation ID.
        message (str): The user’s input message.

    Returns:
        StreamingResponse: SSE stream with a response using uploaded file context.
    """
    return StreamingResponse(
        get_response_with_file(convo_id, message),
        media_type="text/event-stream"
    )

@router.get("/chatbot/version")
def get_chatbot_version(convo_id: str):
    """
    Retrieves the version (A or B) assigned to a conversation for A/B prompt testing.

    Args:
        convo_id (str): The conversation ID.

    Returns:
        dict: A dictionary containing the version (e.g., {"version": "A"}).
    """
    from app.core.chatbot_engine import get_version
    return {"version": get_version(convo_id)}

@router.post("/upload")
async def upload_file(conversation_id: str, file: UploadFile = File(...)):
    """
    Uploads a file, stores it locally, and sends it to OpenAI for use in file-based assistant retrieval.

    Args:
        conversation_id (str): The conversation ID to associate the file with.
        file (UploadFile): The uploaded file from the client.

    Returns:
        dict: Paths to the saved file and the corresponding OpenAI file ID.

    Raises:
        HTTPException: If the file upload or OpenAI integration fails.
    """
    try:
        file_id = str(uuid4())
        file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        print("AQUI ESTÁ")
        openai_file_id = upload_and_store_file(conversation_id, file_path)

        return {"file_path": file_path, "openai_file_id": openai_file_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")