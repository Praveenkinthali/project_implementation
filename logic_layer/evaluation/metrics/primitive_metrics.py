from typing import Dict, List


class PrimitiveMetrics:
    """
    Evaluates effectiveness and behavior of applied primitives.

    Compatible with metadata formats:
    {
        "primitives": [...]
    }

    or

    {
        "primitives_used": [...]
    }
    """

    # ============================================================
    # PUBLIC ENTRY
    # ============================================================

    def compute(self, metadata: Dict) -> Dict:

        # SUPPORT BOTH KEY TYPES
        primitives = metadata.get(
            "primitives_used",
            metadata.get("primitives", [])
        )

        primitive_effect_map = metadata.get("primitive_effect_map", {})

        return {
            "usage_metrics": self._usage_metrics(primitives),
            "diversity_metrics": self._diversity_metrics(primitives),
            "redundancy_metrics": self._redundancy_metrics(primitives),
            "overuse_metrics": self._overuse_metrics(primitives),
            "impact_metrics": self._impact_metrics(primitive_effect_map)
        }

    # ============================================================
    # USAGE METRICS
    # ============================================================

    def _usage_metrics(self, primitives: List[str]) -> Dict:

        return {
            "total_primitives_used": len(primitives),
            "unique_primitives_used": len(set(primitives))
        }

    # ============================================================
    # DIVERSITY METRICS
    # ============================================================

    def _diversity_metrics(self, primitives: List[str]) -> Dict:

        unique = len(set(primitives))
        total = len(primitives)

        diversity_score = unique / total if total else 0

        return {
            "diversity_score": round(diversity_score, 4)
        }

    # ============================================================
    # REDUNDANCY METRICS
    # ============================================================

    def _redundancy_metrics(self, primitives: List[str]) -> Dict:

        freq = {}
        for p in primitives:
            freq[p] = freq.get(p, 0) + 1

        redundant_primitives = [p for p, c in freq.items() if c > 1]

        return {
            "redundant_primitives": redundant_primitives,
            "redundancy_count": len(redundant_primitives)
        }

    # ============================================================
    # OVERUSE METRICS
    # ============================================================

    def _overuse_metrics(self, primitives: List[str]) -> Dict:

        threshold = 6

        return {
            "overuse_flag": len(primitives) > threshold,
            "overuse_threshold": threshold
        }

    # ============================================================
    # IMPACT METRICS
    # ============================================================

    def _impact_metrics(self, primitive_effect_map: Dict[str, float]) -> Dict:

        if not primitive_effect_map:
            return {
                "impact_available": False
            }

        avg_impact = sum(primitive_effect_map.values()) / len(primitive_effect_map)

        high_impact = [
            p for p, score in primitive_effect_map.items()
            if score > avg_impact
        ]

        return {
            "impact_available": True,
            "average_impact": round(avg_impact, 4),
            "high_impact_primitives": high_impact
        }