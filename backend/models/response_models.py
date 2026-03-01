from pydantic import BaseModel
from typing import Dict, Any


class OptimizeResponse(BaseModel):
    run_id: str
    final_score: float
    should_iterate: bool
    optimized_prompt: str
    optimized_response: str
    evaluation: Dict[str, Any]