import math

import pytest

from rbd.evaluator import evaluate_rbd
from rbd.io import validate_document
from rbd.parser import parse_rbd


def test_series():
    components = {
        "A": {"reliability": {"model": "constant", "value": 0.9}},
        "B": {"reliability": {"model": "constant", "value": 0.8}},
    }
    tree = parse_rbd(
        {"type": "series", "blocks": [{"component": "A"}, {"component": "B"}]},
        set(components),
    )
    assert math.isclose(evaluate_rbd(tree, components, 1.0), 0.72)


def test_parallel():
    components = {
        "A": {"reliability": {"model": "constant", "value": 0.9}},
        "B": {"reliability": {"model": "constant", "value": 0.8}},
    }
    tree = parse_rbd(
        {"type": "parallel", "blocks": [{"component": "A"}, {"component": "B"}]},
        set(components),
    )
    assert math.isclose(evaluate_rbd(tree, components, 1.0), 0.98)


def test_reliability_model_is_required():
    document = {
        "components": {"A": {"reliability": {"value": 0.9}}},
        "rbd": {"component": "A"},
    }

    with pytest.raises(ValueError, match="reliability must define 'model'"):
        validate_document(document)
