
import argparse

from esinos.ui.comparison import render_scheduling_comparison

from esinos.scheduling.process import Process
from esinos.scheduling.fcfs import schedule_fcfs
from esinos.scheduling.sjf import schedule_sjf
from esinos.scheduling.summary import SchedulingSummary
from esinos.ui.report import render_scheduling_report


def run_scheduling_demo(algorithm: str) -> None:
    """Run a CPU scheduling demonstration."""

    schedulers = {
        "FCFS": schedule_fcfs,
        "SJF": schedule_sjf,
    }

    algorithm = algorithm.strip().upper()

    scheduler = schedulers.get(algorithm)

    if scheduler is None:
        raise ValueError(
            f"Unsupported scheduling algorithm: {algorithm}"
        )

    # Same processes for both algorithms
    processes = [
        Process("P1", 0, 5),
        Process("P2", 1, 3),
        Process("P3", 2, 1),
    ]

    results, gantt = scheduler(processes)

    summary = SchedulingSummary(
        results=tuple(results),
        gantt=tuple(gantt),
    )

    report = render_scheduling_report(
        summary,
        algorithm,
    )

    print()
    print(report)
    print()


def run_fcfs_demo() -> None:
    """Run the FCFS demonstration."""
    run_scheduling_demo("FCFS")


def run_sjf_demo() -> None:
    """Run the non-preemptive SJF demonstration."""
    run_scheduling_demo("SJF")


def run_comparison_demo() -> None:
    """Compare FCFS and SJF on the same workload."""

    processes = [
        Process("P1", 0, 5),
        Process("P2", 1, 3),
        Process("P3", 2, 1),
    ]

    # Run FCFS
    fcfs_results, fcfs_gantt = schedule_fcfs(processes)

    fcfs_summary = SchedulingSummary(
        results=tuple(fcfs_results),
        gantt=tuple(fcfs_gantt),
    )

    # Run SJF
    sjf_results, sjf_gantt = schedule_sjf(processes)

    sjf_summary = SchedulingSummary(
        results=tuple(sjf_results),
        gantt=tuple(sjf_gantt),
    )

    # Build and display the comparison
    report = render_scheduling_comparison(
        fcfs_summary,
        sjf_summary,
    )

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
        print("[2] CPU Scheduling - SJF Demo")
        print("[3] Compare FCFS vs SJF")
        print("[0] Exit")
        print()

        try:
            choice = input("Select an option: ").strip()

        except (EOFError, KeyboardInterrupt):
            print("\nExiting ESINOS.")
            return 0

        if choice == "1":
            run_fcfs_demo()

        elif choice == "2":
            run_sjf_demo()
        

        elif choice == "3":
            run_comparison_demo()


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

    demo_group = parser.add_mutually_exclusive_group()

    demo_group.add_argument(
        "--demo-fcfs",
        action="store_true",
        help="Run the FCFS demonstration",
    )

    demo_group.add_argument(
        "--demo-sjf",
        action="store_true",
        help="Run the SJF demonstration",
    )

    demo_group.add_argument(
        "--compare-fcfs-sjf",
        action="store_true",
        help="Compare FCFS and SJF on the same workload",
    )

    args = parser.parse_args()

    if args.demo_fcfs:
        run_fcfs_demo()
        return 0

    if args.demo_sjf:
        run_sjf_demo()
        return 0

    if args.compare_fcfs_sjf:
        run_comparison_demo()
        return 0
        
    return run_menu()


if __name__ == "__main__":
    raise SystemExit(main())
