from logic_layer.evaluation.metrics.primitive_metrics import PrimitiveMetrics
from pprint import pprint


def print_section(title):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def display_clean_metrics(result):
    print("\n📊 USAGE METRICS")
    pprint(result["usage_metrics"])

    print("\n🎯 DIVERSITY METRICS")
    pprint(result["diversity_metrics"])

    print("\n🔁 REDUNDANCY METRICS")
    pprint(result["redundancy_metrics"])

    print("\n⚠️ OVERUSE METRICS")
    pprint(result["overuse_metrics"])

    print("\n🚀 IMPACT METRICS")
    pprint(result["impact_metrics"])


def run_test_cases():

    pm = PrimitiveMetrics()

    test_cases = [

        # ----------------------------------------------------------
        # 1. Balanced Primitive Use
        # ----------------------------------------------------------
        {
            "name": "Balanced Primitive Usage",
            "metadata": {
                "primitives_used": [
                    "Clarify",
                    "FormatEnforce",
                    "AddExample"
                ],
                "primitive_effect_map": {
                    "Clarify": 0.4,
                    "FormatEnforce": 0.3,
                    "AddExample": 0.5
                }
            }
        },

        # ----------------------------------------------------------
        # 2. Redundant Primitive Usage
        # ----------------------------------------------------------
        {
            "name": "Redundant Primitive Usage",
            "metadata": {
                "primitives_used": [
                    "Clarify",
                    "Clarify",
                    "FormatEnforce"
                ]
            }
        },

        # ----------------------------------------------------------
        # 3. Overuse Scenario
        # ----------------------------------------------------------
        {
            "name": "Overuse Scenario",
            "metadata": {
                "primitives_used": [
                    "Clarify",
                    "FormatEnforce",
                    "AddExample",
                    "Decompose",
                    "ConstrainOutput",
                    "ScopeAlign",
                    "SelfReflect"
                ]
            }
        },

        # ----------------------------------------------------------
        # 4. No Primitive Used
        # ----------------------------------------------------------
        {
            "name": "No Primitive Used",
            "metadata": {
                "primitives_used": []
            }
        }
    ]

    for case in test_cases:

        print_section(f"🧪 TEST CASE: {case['name']}")

        result = pm.compute(case["metadata"])

        print("\n🔹 INPUT METADATA:")
        pprint(case["metadata"])

        display_clean_metrics(result)


if __name__ == "__main__":
    run_test_cases()