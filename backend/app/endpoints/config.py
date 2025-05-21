from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.prompt_config import load_prompts, update_prompt

router = APIRouter()

class PromptUpdate(BaseModel):
    version: str  # should be "A" or "B"
    prompt: str

@router.get("/")
def get_prompts():
    return load_prompts()

@router.put("/")
def set_prompt(update: PromptUpdate):
    if update.version not in ("A", "B"):
        raise HTTPException(status_code=400, detail="Version must be A or B")
    update_prompt(update.version, update.prompt)
    return {"status": "updated"}
