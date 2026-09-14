from __future__ import annotations

import math
from typing import Any, Mapping


def component_reliability(model: Mapping[str, Any], t: float) -> float:
    """Return component reliability R(t) for a supported reliability model."""
    if t < 0:
        raise ValueError("Mission time must be non-negative.")

    distribution = str(model.get("distribution", "")).lower()

    if distribution == "exponential":
        try:
            lambda_ = float(model["lambda"])
        except KeyError as exc:
            raise ValueError("Exponential model requires parameter 'lambda'.") from exc
        if lambda_ < 0:
            raise ValueError("Parameter 'lambda' must be non-negative.")
        return math.exp(-lambda_ * t)

    if distribution == "weibull":
        try:
            beta = float(model["beta"])
            eta = float(model["eta"])
        except KeyError as exc:
            raise ValueError("Weibull model requires parameters 'beta' and 'eta'.") from exc
        if beta <= 0 or eta <= 0:
            raise ValueError("Weibull parameters 'beta' and 'eta' must be positive.")
        return math.exp(-((t / eta) ** beta))

    if distribution == "constant":
        try:
            reliability = float(model["value"])
        except KeyError as exc:
            raise ValueError("Constant model requires parameter 'value'.") from exc
        if not 0.0 <= reliability <= 1.0:
            raise ValueError("Constant reliability 'value' must be in [0, 1].")
        return reliability

    raise ValueError(f"Unsupported reliability distribution: {distribution!r}")
