
import argparse

from esinos.ui.comparison import render_scheduling_comparison

from esinos.scheduling.rr import schedule_rr

from esinos.scheduling.priority import schedule_priority


from esinos.ui.comparison_three import render_three_way_comparison


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

def run_rr_demo(quantum: int = 3) -> None:
    """Run a Round Robin demonstration."""

    processes = [
        Process("P1", 0, 5),
        Process("P2", 1, 3),
        Process("P3", 2, 1),
    ]

    results, gantt = schedule_rr(
        processes,
        quantum,
    )

    summary = SchedulingSummary(
        results=tuple(results),
        gantt=tuple(gantt),
    )

    report = render_scheduling_report(
        summary,
        "RR",
    )

    print()
    print(f"Time quantum: {quantum}")
    print()
    print(report)
    print()


def run_three_way_comparison_demo(
    quantum: int = 2,
) -> None:
    """Compare FCFS, SJF and RR on the same workload."""

    processes = [
        Process("P1", 0, 5),
        Process("P2", 1, 3),
        Process("P3", 2, 1),
    ]

    # FCFS
    fcfs_results, fcfs_gantt = schedule_fcfs(processes)

    fcfs_summary = SchedulingSummary(
        results=tuple(fcfs_results),
        gantt=tuple(fcfs_gantt),
    )

    # SJF
    sjf_results, sjf_gantt = schedule_sjf(processes)

    sjf_summary = SchedulingSummary(
        results=tuple(sjf_results),
        gantt=tuple(sjf_gantt),
    )

    # Round Robin
    rr_results, rr_gantt = schedule_rr(
        processes,
        quantum,
    )

    rr_summary = SchedulingSummary(
        results=tuple(rr_results),
        gantt=tuple(rr_gantt),
    )

    # Generate comparative report
    report = render_three_way_comparison(
        fcfs_summary,
        sjf_summary,
        rr_summary,
        quantum,
    )

    print()
    print(report)
    print()


def run_priority_demo() -> None:
    """Run non-preemptive Priority Scheduling demo."""

    processes = [
        Process("P1", 0, 6, priority=3),
        Process("P2", 1, 2, priority=1),
        Process("P3", 2, 4, priority=2),
        Process("P4", 4, 1, priority=1),
    ]

    # Step 1: Execute Priority Scheduling
    results, gantt = schedule_priority(processes)

    # Step 2: Build scheduling summary
    summary = SchedulingSummary(
        results=tuple(results),
        gantt=tuple(gantt),
    )

    # Step 3: Generate report
    report = render_scheduling_report(
        summary,
        "PRIORITY",
    )

    print()
    print("Priority Scheduling (Non-Preemptive)")
    print("Priority rule: lower number = higher priority")
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
        print("[4] CPU Scheduling - Round Robin")
        print("[5] Compare FCFS vs SJF vs RR")
        print("[6] CPU Scheduling - Priority Demo")
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

        elif choice == "4":
            try:
                quantum_text = input(
                    "RR quantum [default 3]: "
                ).strip()

            except (EOFError, KeyboardInterrupt):
                print("\nExiting ESINOS.")
                return 0

            try:
                quantum = (
                    int(quantum_text)
                    if quantum_text
                    else 3
                )

            except ValueError:
                print(
                    "Invalid quantum. Enter a positive integer."
                )
                continue

            if quantum <= 0:
                print(
                    "Invalid quantum. Enter a positive integer."
                )
                continue

            run_rr_demo(quantum)

        elif choice == "5":
            try:
                quantum_text = input(
                    "Comparison RR quantum [default 2]: "
                ).strip()

            except (EOFError, KeyboardInterrupt):
                print("\nExiting ESINOS.")
                return 0

            try:
                quantum = (
                    int(quantum_text)
                    if quantum_text
                    else 2
                )

            except ValueError:
                print(
                    "Invalid quantum. Enter a positive integer."
                )
                continue

            if quantum <= 0:
                print(
                    "Invalid quantum. Enter a positive integer."
                )
                continue

            run_three_way_comparison_demo(quantum)
        
        elif choice == "6":
            run_priority_demo()

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
        "--demo-priority",
        action="store_true",
        help="Run non-preemptive Priority Scheduling demo",
)

    demo_group.add_argument(
        "--demo-fcfs",
        action="store_true",
        help="Run FCFS demonstration",
    )

    demo_group.add_argument(
        "--demo-sjf",
        action="store_true",
        help="Run SJF demonstration",
    )

    demo_group.add_argument(
        "--compare-fcfs-sjf",
        action="store_true",
        help="Compare FCFS and SJF",
    )

    demo_group.add_argument(
        "--demo-rr",
        action="store_true",
        help="Run Round Robin demonstration",
    )

    demo_group.add_argument(
        "--compare-all",
        action="store_true",
        help="Compare FCFS, SJF and Round Robin",
    )

    parser.add_argument(
        "--quantum",
        type=int,
        default=None,
        help="Positive RR quantum for demo or comparison",
    )

    args = parser.parse_args()

    # Validate quantum usage
    if args.quantum is not None:
        if not (args.demo_rr or args.compare_all):
            parser.error(
                "--quantum requires --demo-rr or --compare-all"
            )

        if args.quantum <= 0:
            parser.error(
                "--quantum must be a positive integer"
            )

    # Dispatch execution modes
    if args.demo_fcfs:
        run_fcfs_demo()
        return 0

    if args.demo_sjf:
        run_sjf_demo()
        return 0

    if args.compare_fcfs_sjf:
        run_comparison_demo()
        return 0

    if args.demo_rr:
        quantum = (
            args.quantum
            if args.quantum is not None
            else 3
        )

        run_rr_demo(quantum)
        return 0

    if args.compare_all:
        quantum = (
            args.quantum
            if args.quantum is not None
            else 2
        )

        run_three_way_comparison_demo(quantum)
        return 0
    
    if args.demo_priority:
        run_priority_demo()
        return 0

    return run_menu()

if __name__ == "__main__":
    raise SystemExit(main())
