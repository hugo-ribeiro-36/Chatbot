from app.db.database import db_session
from app.db.models import PromptConfig


def load_prompts() -> dict:
    prompts = db_session.query(PromptConfig).all()
    return {p.version: p.prompt for p in prompts}

def update_prompt(version: str, prompt: str):
    config = db_session.query(PromptConfig).filter_by(version=version).first()
    if config:
        config.prompt = prompt  
    else:
        config = PromptConfig(version=version, prompt=prompt)
        db_session.add(config)
        db_session.commit()
