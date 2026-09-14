from __future__ import annotations

import argparse
import sys

from rbd import component_results, evaluate_rbd, load_yaml, parse_rbd, validate_document


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Read an RBD described in YAML and calculate system reliability."
    )
    parser.add_argument("yaml_file", help="Path to the RBD YAML file.")
    parser.add_argument(
        "--time",
        "-t",
        type=float,
        default=None,
        help="Mission time. Overrides analysis.mission_time from the YAML file.",
    )
    parser.add_argument(
        "--components",
        action="store_true",
        help="Also print the reliability of each component.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    try:
        data = load_yaml(args.yaml_file)
        validate_document(data)

        components = data["components"]
        tree = parse_rbd(data["rbd"], set(components))

        if args.time is not None:
            mission_time = args.time
        else:
            analysis = data.get("analysis", {})
            if "mission_time" not in analysis:
                raise ValueError(
                    "Mission time not provided. Use '--time' or define analysis.mission_time in YAML."
                )
            mission_time = float(analysis["mission_time"])

        reliability = evaluate_rbd(tree, components, mission_time)

        system_name = data.get("system", {}).get("name", "Unnamed system")
        time_unit = data.get("analysis", {}).get("time_unit", "time units")

        print(f"System: {system_name}")
        print(f"Mission time: {mission_time:g} {time_unit}")
        print(f"System reliability: {reliability:.10f}")

        if args.components:
            print("\nComponent reliabilities:")
            for component_id, value in component_results(components, mission_time).items():
                print(f"  {component_id}: {value:.10f}")

        return 0

    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
