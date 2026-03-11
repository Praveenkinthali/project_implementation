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

    # get last iteration safely
    iterations = result.get("iterations", [])
    iteration = iterations[-1] if iterations else {}

    evaluation = iteration.get("evaluation", {})

    return {

        "run_id": str(result.get("_id")),

        "optimized_prompt": iteration.get("optimized_prompt"),
        "optimized_response": iteration.get("optimized_response"),

        # ===== METRICS (safe extraction) =====

        "latency_original": iteration.get("latency_original"),
        "latency_optimized": iteration.get("latency_optimized"),

        "tokens_original": iteration.get("tokens_original"),
        "tokens_optimized": iteration.get("tokens_optimized"),

        # ===== EVALUATION =====

        "evaluation": evaluation,

        "final_score": evaluation.get("final_score", 0.0),

        "should_iterate": evaluation.get("should_iterate", False)
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
        "response": result.get("response"),
        "latency": result.get("latency"),
        "tokens": result.get("tokens")
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