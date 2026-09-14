from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class ComponentNode:
    component_id: str


@dataclass(frozen=True)
class LogicNode:
    logic_type: str
    children: tuple["RBDNode", ...]


RBDNode = ComponentNode | LogicNode


def parse_rbd(block: Mapping[str, Any], known_components: set[str]) -> RBDNode:
    """Parse a YAML RBD block into an internal tree representation."""
    if "component" in block:
        component_id = str(block["component"])
        if component_id not in known_components:
            raise ValueError(f"RBD references unknown component {component_id!r}.")
        return ComponentNode(component_id=component_id)

    logic_type = str(block.get("type", "")).lower()
    if logic_type not in {"series", "parallel"}:
        raise ValueError(
            "Each logic block must have type 'series' or 'parallel', "
            "or declare a 'component'."
        )

    raw_children = block.get("blocks")
    if not isinstance(raw_children, list) or not raw_children:
        raise ValueError(f"Logic block {logic_type!r} must contain a non-empty 'blocks' list.")

    children = tuple(parse_rbd(child, known_components) for child in raw_children)
    return LogicNode(logic_type=logic_type, children=children)
