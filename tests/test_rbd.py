import math

from rbd.evaluator import evaluate_rbd
from rbd.parser import parse_rbd


def test_series():
    components = {
        "A": {"reliability": {"distribution": "constant", "value": 0.9}},
        "B": {"reliability": {"distribution": "constant", "value": 0.8}},
    }
    tree = parse_rbd(
        {"type": "series", "blocks": [{"component": "A"}, {"component": "B"}]},
        set(components),
    )
    assert math.isclose(evaluate_rbd(tree, components, 1.0), 0.72)


def test_parallel():
    components = {
        "A": {"reliability": {"distribution": "constant", "value": 0.9}},
        "B": {"reliability": {"distribution": "constant", "value": 0.8}},
    }
    tree = parse_rbd(
        {"type": "parallel", "blocks": [{"component": "A"}, {"component": "B"}]},
        set(components),
    )
    assert math.isclose(evaluate_rbd(tree, components, 1.0), 0.98)
