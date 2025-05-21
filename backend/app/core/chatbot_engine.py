import os
import random
from openai import OpenAI
from app.core.knowledge_vector import search_knowledge_vector
from app.core.prompt_config import load_prompts
from app.db.models import PromptConfig, Conversation, Message
from app.db.database import db_session

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key = api_key)

conversation_memory = {}

async def get_streaming_response(convo_id: str, user_msg: str):
    """
    Handles a streaming chat response using GPT-3.5, integrating knowledge base chunks when relevant.

    Args:
        convo_id (str): Unique identifier of the conversation.
        user_msg (str): The user's message.

    Yields:
        str: Streaming tokens as Server-Sent Events (SSE) for real-time UI updates.
    """
    conv = db_session.query(Conversation).filter_by(id=convo_id).first()

    if not conv.version:
        version = random.choice(["A", "B"])
        conv.version = version
        db_session.commit()

    db_session.add(Message(conversation_id=convo_id, role="user", content=user_msg))
    db_session.commit()

    prompt_row = db_session.query(PromptConfig).filter_by(version=conv.version).first()
    system_prompt = prompt_row.prompt if prompt_row else "You are a helpful assistant."

    messages = conversation_memory.get(convo_id, [])
    if not messages:
        messages.append({"role": "system", "content": system_prompt})


    relevant_chunks = search_knowledge_vector(user_msg)
    #print("Search result:", relevant_chunks)

    if relevant_chunks:
        messages.append({
            "role": "system",
            "content": (
                    "Take into account the following knowledge base information. "
                    "If it directly answers the user’s question, respond using only this. "
                    "Otherwise, use your own general knowledge to answer appropriately.\n\n"
                    + "\n\n".join(relevant_chunks)
            )
        })

    messages.append({"role": "user", "content": user_msg})
    
    #print(messages)

    try:
        response = client.responses.create(
            model="gpt-3.5-turbo",
            input=messages,
            stream=True,
        )
        full_reply = ""
        for chunk in response:
            if chunk.type == "response.output_text.delta":
                token = chunk.delta
                full_reply += token
                yield f"data: {token}\n\n"

            # Optionally detect done signal
            if chunk.type == "response.output_text.done":
                break

        db_session.add(Message(conversation_id=convo_id, role="assistant", content=full_reply))
        db_session.commit()
        messages.append({"role": "assistant", "content": full_reply})
        conversation_memory[convo_id] = messages

    except Exception as e:
        yield f"data: [Error: {str(e)}]\n\n"

async def get_web_response(convo_id: str, user_msg: str):
    """
    Handles a streaming response using GPT-4.1 with web search tool enabled.

    Args:
        convo_id (str): Unique identifier of the conversation.
        user_msg (str): The user's message.

    Yields:
        str: Streaming tokens with potential web-sourced context via SSE.
    """
    conv = db_session.query(Conversation).filter_by(id=convo_id).first()

    if not conv.version:
        version = random.choice(["A", "B"])
        conv.version = version
        db_session.commit()

    db_session.add(Message(conversation_id=convo_id, role="user", content=user_msg))
    db_session.commit()

    prompt_row = db_session.query(PromptConfig).filter_by(version=conv.version).first()
    system_prompt = prompt_row.prompt if prompt_row else "You are a helpful assistant."

    messages = conversation_memory.get(convo_id, [])
    if not messages:
        messages.append({"role": "system", "content": system_prompt})


    messages.append({"role": "user", "content": user_msg})
    print(messages)

    try:
        response = client.responses.create(
            model="gpt-4.1",
            tools=[{"type": "web_search_preview"}],
            input=messages,
            stream=True,
        )
        full_reply = ""
        for chunk in response:
            if chunk.type == "response.output_text.delta":
                token = chunk.delta
                full_reply += token
                yield f"data: {token}\n\n"

            # Optionally detect done signal
            if chunk.type == "response.output_text.done":
                break

        db_session.add(Message(conversation_id=convo_id, role="assistant", content=full_reply))
        db_session.commit()
        messages.append({"role": "assistant", "content": full_reply})
        conversation_memory[convo_id] = messages

    except Exception as e:
        yield f"data: [Error: {str(e)}]\n\n"



def create_file_based_assistant(file_id: str) -> str:
    """
    Creates an OpenAI Assistant instance configured with a specific uploaded file for retrieval.

    Args:
        file_id (str): The ID of the uploaded file (from OpenAI's file API).

    Returns:
        str: The created assistant's ID.
    """
    assistant = client.beta.assistants.create(
        name="File Assistant",
        instructions="Use the uploaded documents to answer questions.",
        tools=[{"type": "retrieval"}],
        model="gpt-4-1106-preview",
        file_ids=[file_id]
    )
    return assistant.id



def upload_and_store_file(conversation_id: str, file_path: str) -> str:
    """
    Uploads a file to OpenAI's API and links it to the conversation in the database.

    Args:
        conversation_id (str): The conversation to associate the file with.
        file_path (str): Local path to the file to upload.

    Returns:
        str: The OpenAI-generated file ID.
    """
    with open(file_path, "rb") as f:
        file = client.files.create(file=f, purpose="assistants")

    print(file)
    convo = db_session.query(Conversation).filter_by(id=conversation_id).first()
    if convo:
        convo.file_id = file.id
        db_session.commit()

    return file.id

async def get_response_with_file(conversation_id: str, user_message: str):
    """
    Streams a response from an OpenAI Assistant using file-based retrieval for the given conversation.

    Args:
        conversation_id (str): The conversation ID linked to the uploaded file.
        user_message (str): The message to send to the Assistant.

    Yields:
        str: Streaming tokens from the assistant's response via SSE.
    """
    convo = db_session.query(Conversation).filter_by(id=conversation_id).first()
    file_id = convo.file_id if convo else None
    version = get_version(conversation_id)

    assistant = client.beta.assistants.create(
        name="Knowledge Assistant",
        instructions="Use the uploaded file to answer.",
        tools=[{"type": "file_search"}],
        model="gpt-3.5-turbo",
    )

    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_message,
        attachments= [{ "file_id": file_id, "tools": [{"type": "file_search"}]}],
    )
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)

    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if run_status.status == "completed":
            break

    messages = client.beta.threads.messages.list(thread_id=thread.id)
    print(messages)
    for msg in reversed(messages.data):
        if msg.role == "assistant":
            reply = msg.content[0].text.value
            for token in reply:
                yield f"data: {token}\n\n"
            break


def get_version(convo_id: str) -> str:
    return db_session.query(Conversation).filter_by(id=convo_id).first().version



