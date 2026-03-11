from pydantic import BaseModel
from typing import Dict, Any


class OptimizeResponse(BaseModel):

    run_id: str

    optimized_prompt: str
    optimized_response: str

    latency_original: float | None = None
    latency_optimized: float | None = None

    tokens_original: int | None = None
    tokens_optimized: int | None = None

    evaluation: dict

    final_score: float
    should_iterate: bool