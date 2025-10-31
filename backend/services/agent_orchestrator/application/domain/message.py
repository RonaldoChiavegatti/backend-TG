from pydantic import BaseModel


class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str
