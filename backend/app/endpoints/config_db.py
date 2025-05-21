from fastapi import APIRouter, HTTPException
from app.schemas.config import PromptConfigCreate
from app.db.database import db_session
from app.db.models import PromptConfig

router = APIRouter()

@router.get("/")
def get_prompts():
    """
    Retrieves all system prompts for each version (A/B).

    Returns:
        dict: A dictionary mapping version strings to their corresponding prompt texts.
    """
    prompts = db_session.query(PromptConfig).all()
    return {p.version: p.prompt for p in prompts}

@router.put("/")
def update_prompt(config: PromptConfigCreate):
    """
    Creates or updates the system prompt for a given version.

    If a prompt for the version already exists, it is updated.
    Otherwise, a new record is created.

    Args:
        config (PromptConfigCreate): Object containing `version` and `prompt`.

    Returns:
        dict: A status message indicating success.
    """
    prompt = db_session.query(PromptConfig).filter_by(version=config.version).first()
    if not prompt:
        prompt = PromptConfig(version=config.version, prompt=config.prompt)
        db_session.add(prompt)
    else:
        prompt.prompt = config.prompt
    db_session.commit()
    return {"status": "updated"}
