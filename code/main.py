import argparse

from esinos.scheduling.process import Process
from esinos.scheduling.fcfs import schedule_fcfs
from esinos.scheduling.summary import SchedulingSummary
from esinos.ui.report import render_scheduling_report


def run_fcfs_demo() -> None:
    """Run a predefined FCFS demonstration."""

    processes = [
        Process("P1", 0, 5),
        Process("P2", 1, 3),
        Process("P3", 2, 1),
    ]

    results, gantt = schedule_fcfs(processes)

    summary = SchedulingSummary(
        results=tuple(results),
        gantt=tuple(gantt),
    )

    report = render_scheduling_report(summary, "FCFS")

    print()
    print(report)
    print()


def run_menu() -> int:
    """Display the interactive ESINOS main menu."""

    while True:
        print()
        print("=" * 46)
        print("       ESINOS - OS Simulator")
        print("=" * 46)
        print()
        print("MAIN MENU")
        print()
        print("[1] CPU Scheduling - FCFS Demo")
        print("[0] Exit")
        print()

        try:
            choice = input("Select an option: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting ESINOS.")
            return 0

        if choice == "1":
            run_fcfs_demo()

        elif choice == "0":
            print("Exiting ESINOS.")
            return 0

        else:
            print("Invalid option. Please try again.")


def main() -> int:
    """ESINOS application entry point."""

    parser = argparse.ArgumentParser(
        description="ESINOS - Educational OS Simulator"
    )

    parser.add_argument(
        "--demo-fcfs",
        action="store_true",
        help="Run the FCFS demonstration directly",
    )

    args = parser.parse_args()

    if args.demo_fcfs:
        run_fcfs_demo()
        return 0

    return run_menu()


if __name__ == "__main__":
    raise SystemExit(main())
