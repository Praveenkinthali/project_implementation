from db.repositories.run_repository import RunRepository
from logic_layer.refiner.single_pass_refiner import SinglePassRefiner
from logic_layer.evaluation.evaluator import Evaluator
from services.llm_service import LLMService


class PipelineService:

    @staticmethod
    async def run_pipeline(prompt: str, user_id: str):

        # -----------------------------
        # 1️⃣ Create Run Entry
        # -----------------------------
        run_id = await RunRepository.create_run(
            user_id=user_id,
            original_prompt=prompt,
            model_used="groq"
        )

        llm_service = LLMService()
        refiner = SinglePassRefiner()

        # -----------------------------
        # 2️⃣ Generate Original Response
        # -----------------------------
        original_llm_result = llm_service.generate(prompt)
        original_response = original_llm_result["output"]

        # -----------------------------
        # 3️⃣ Optimize Prompt
        # -----------------------------
        optimized_prompt, metadata = refiner.refine(prompt)

        # -----------------------------
        # 4️⃣ Generate Optimized Response
        # -----------------------------
        optimized_llm_result = llm_service.generate(optimized_prompt)
        optimized_response = optimized_llm_result["output"]

        # -----------------------------
        # 5️⃣ Evaluate
        # -----------------------------
        evaluator = Evaluator(llm=llm_service.llm)

        evaluation_result = evaluator.evaluate(
            original_prompt=prompt,
            optimized_prompt=optimized_prompt,
            original_response=original_response,
            optimized_response=optimized_response,
            metadata=metadata
        )

        # -----------------------------
        # 6️⃣ Log Iteration
        # -----------------------------
        await RunRepository.add_iteration(run_id, {
            "iteration": 1,
            "optimized_prompt": optimized_prompt,
            "original_response": original_response,
            "optimized_response": optimized_response,
            "evaluation": evaluation_result,
            "latency_original": original_llm_result["latency"],
            "latency_optimized": optimized_llm_result["latency"],
            "tokens_original": original_llm_result["tokens_used"],
            "tokens_optimized": optimized_llm_result["tokens_used"],
        })

        # -----------------------------
        # 7️⃣ Finalize Run
        # -----------------------------
        await RunRepository.finalize_run(
            run_id,
            final_prompt=optimized_prompt,
            final_response=optimized_response
        )

        return await RunRepository.get_run(run_id, user_id)


    # ============================================================
    # A/B TEST GENERATION
    # ============================================================

    @staticmethod
    async def generate_only(prompt: str):

        llm_service = LLMService()

        llm_result = llm_service.generate(prompt)

        return {
            "response": llm_result["output"],
            "latency": llm_result["latency"],
            "tokens": llm_result["tokens_used"]
        }