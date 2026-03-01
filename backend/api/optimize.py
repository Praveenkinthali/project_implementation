from fastapi import APIRouter
from services.pipeline_service import PipelineService
from models.request_models import OptimizeRequest
from models.response_models import OptimizeResponse
from db.repositories.run_repository import RunRepository

router = APIRouter()


@router.post("/optimize", response_model=OptimizeResponse)
async def optimize(request: OptimizeRequest):

    result = await PipelineService.run_pipeline(request.prompt)

    iteration = result["iterations"][-1]

    return {
        "run_id": result["_id"],
        "final_score": iteration["evaluation"]["final_score"],
        "should_iterate": iteration["evaluation"]["should_iterate"],
        "optimized_prompt": iteration["optimized_prompt"],
        "optimized_response": iteration["optimized_response"],
        "evaluation": iteration["evaluation"]
    }


@router.get("/runs")
async def list_runs():
    return await RunRepository.list_runs()


@router.get("/runs/{run_id}")
async def get_run(run_id: str):
    return await RunRepository.get_run(run_id)