from __future__ import annotations

import math
from typing import Any, Mapping

from .models import component_reliability
from .parser import ComponentNode, LogicNode, RBDNode


def evaluate_rbd(node: RBDNode, components: Mapping[str, Any], t: float) -> float:
    """Evaluate the reliability of an RBD tree at mission time t."""
    if isinstance(node, ComponentNode):
        component = components[node.component_id]
        return component_reliability(component["reliability"], t)

    if isinstance(node, LogicNode):
        reliabilities = [evaluate_rbd(child, components, t) for child in node.children]

        if node.logic_type == "series":
            return math.prod(reliabilities)

        if node.logic_type == "parallel":
            return 1.0 - math.prod(1.0 - r for r in reliabilities)

    raise TypeError(f"Unsupported RBD node: {node!r}")


def component_results(components: Mapping[str, Any], t: float) -> dict[str, float]:
    """Evaluate every declared component at mission time t."""
    return {
        component_id: component_reliability(data["reliability"], t)
        for component_id, data in components.items()
    }
