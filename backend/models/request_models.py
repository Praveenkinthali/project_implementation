from pydantic import BaseModel


class OptimizeRequest(BaseModel):
    prompt: str