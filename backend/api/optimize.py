from fastapi import APIRouter, Depends
from services.pipeline_service import PipelineService
from models.request_models import OptimizeRequest
from models.response_models import OptimizeResponse
from db.repositories.run_repository import RunRepository
from utils.dependencies import get_current_user

router = APIRouter()


# ============================================================
# OPTIMIZATION PIPELINE (PROTECTED)
# ============================================================

@router.post("/optimize", response_model=OptimizeResponse)
async def optimize(
    request: OptimizeRequest,
    current_user: dict = Depends(get_current_user)
):

    result = await PipelineService.run_pipeline(
        request.prompt,
        user_id=str(current_user["_id"])
    )

    iteration = result["iterations"][-1]

    return {
        "run_id": result["_id"],
        "final_score": iteration["evaluation"]["final_score"],
        "should_iterate": iteration["evaluation"]["should_iterate"],
        "optimized_prompt": iteration["optimized_prompt"],
        "optimized_response": iteration["optimized_response"],
        "evaluation": iteration["evaluation"]
    }


# ============================================================
# DIRECT GENERATION (A/B TESTING)
# ============================================================

@router.post("/generate")
async def generate(
    request: OptimizeRequest,
    current_user: dict = Depends(get_current_user)
):

    result = await PipelineService.generate_only(request.prompt)

    return {
        "response": result["response"],
        "latency": result["latency"],
        "tokens": result["tokens"]
    }


# ============================================================
# RUN HISTORY
# ============================================================

@router.get("/runs")
async def list_runs(
    current_user: dict = Depends(get_current_user)
):

    return await RunRepository.list_runs(
        user_id=str(current_user["_id"])
    )


@router.get("/runs/{run_id}")
async def get_run(
    run_id: str,
    current_user: dict = Depends(get_current_user)
):

    return await RunRepository.get_run(
        run_id,
        user_id=str(current_user["_id"])
    )