import importlib
import traceback


SCENARIOS = [
    "scenario_1",
    "scenario_2",
    "scenario_3",
]


def main() -> int:
    failed = 0

    for scenario_name in SCENARIOS:
        try:
            scenario = importlib.import_module(scenario_name)
            scenario.run()
        except Exception:
            failed += 1
            print(f"FAIL {scenario_name}")
            traceback.print_exc()
        else:
            print(f"PASS {scenario_name}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
