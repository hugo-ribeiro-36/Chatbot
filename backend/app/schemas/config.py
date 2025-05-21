from pydantic import BaseModel

class PromptConfigCreate(BaseModel):
    version: str
    prompt: str
