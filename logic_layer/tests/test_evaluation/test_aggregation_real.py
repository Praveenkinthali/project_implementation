from pprint import pprint
from logic_layer.evaluation.metrics.aggregation import AggregationEngine


def run_aggregation_test():

    agg = AggregationEngine()

    mock_metrics = {
        "prompt_metrics": {},
        "primitive_metrics": {},
        "response_metrics": {},
        "semantic_metrics": {
            "prompt_semantic_similarity": 0.8,
            "prompt_response_alignment": 0.75
        },
        "judge_metrics": {
            "overall_quality": 8
        }
    }

    print("\n" + "=" * 100)
    print("AGGREGATION TEST")
    print("=" * 100)

    result = agg.compute_final_score(mock_metrics)
    pprint(result)


if __name__ == "__main__":
    run_aggregation_test()