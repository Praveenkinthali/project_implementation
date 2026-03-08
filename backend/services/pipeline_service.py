from db.repositories.run_repository import RunRepository
from logic_layer.refiner.single_pass_refiner import SinglePassRefiner
from logic_layer.evaluation.evaluator import Evaluator
from logic_layer.evaluation.feedback_store import FeedbackStore
from logic_layer.evaluation.adaptive_learning import AdaptiveLearningEngine
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

        feedback_store = FeedbackStore()
        learning_engine = AdaptiveLearningEngine()

        # -----------------------------
        # 2️⃣ Generate Original Response
        # -----------------------------
        original_llm_result = llm_service.generate(prompt)
        original_response = original_llm_result["output"]

        # -----------------------------
        # 3️⃣ Optimize Prompt
        # -----------------------------
        optimized_prompt, metadata = refiner.refine(prompt)

        # Extract primitives used
        primitives_used = metadata.get("applied_primitives") or metadata.get("selected_primitives") or []

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

        # Extract final score safely
        final_score = evaluation_result.get("final_score") or evaluation_result.get("score", 0.0)

        # -----------------------------
        # 6️⃣ RL LEARNING UPDATE
        # -----------------------------
        try:

            learning_engine.record(primitives_used, final_score)

            feedback_store.store(
                session_id=str(run_id),
                final_score=final_score,
                primitives=primitives_used,
                user_rating=None,
                comment=None
            )

            print("✅ Learning recorded:", primitives_used, final_score)

        except Exception as e:

            print("⚠️ Learning update failed:", e)

        # -----------------------------
        # 7️⃣ Log Iteration (MongoDB)
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
        # 8️⃣ Finalize Run
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