from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_yaml(path: str | Path) -> dict[str, Any]:
    yaml_path = Path(path)
    with yaml_path.open("r", encoding="utf-8") as stream:
        data = yaml.safe_load(stream)

    if not isinstance(data, dict):
        raise ValueError("Top-level YAML content must be a mapping/object.")

    return data


def validate_document(data: dict[str, Any]) -> None:
    components = data.get("components")
    if not isinstance(components, dict) or not components:
        raise ValueError("YAML must contain a non-empty 'components' mapping.")

    for component_id, component in components.items():
        if not isinstance(component, dict):
            raise ValueError(f"Component {component_id!r} must be a mapping/object.")
        if "reliability" not in component:
            raise ValueError(f"Component {component_id!r} must define 'reliability'.")
        if not isinstance(component["reliability"], dict):
            raise ValueError(f"Component {component_id!r} reliability must be a mapping/object.")

    if not isinstance(data.get("rbd"), dict):
        raise ValueError("YAML must contain an 'rbd' mapping/object.")
