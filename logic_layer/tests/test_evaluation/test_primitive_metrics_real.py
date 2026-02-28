from pprint import pprint
from logic_layer.evaluation.metrics.primitive_metrics import PrimitiveMetrics


def run_primitive_metrics_test():

    primitive_metrics = PrimitiveMetrics()

    metadata = {
        "primitives_used": [
            "Clarify",
            "FormatEnforce",
            "AddExample"
        ],
        "primitive_effect_map": {
            "Clarify": 0.3,
            "FormatEnforce": 0.5,
            "AddExample": 0.4
        }
    }

    print("\n" + "=" * 100)
    print("PRIMITIVE METRICS TEST")
    print("=" * 100)

    result = primitive_metrics.compute(metadata)
    pprint(result)


if __name__ == "__main__":
    run_primitive_metrics_test()