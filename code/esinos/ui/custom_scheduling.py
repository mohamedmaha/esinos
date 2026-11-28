from collections.abc import Callable

from esinos.ui.comparison_four import render_four_way_comparison

from esinos.scheduling.fcfs import schedule_fcfs
from esinos.scheduling.sjf import schedule_sjf
from esinos.scheduling.rr import schedule_rr
from esinos.scheduling.priority import schedule_priority
from esinos.scheduling.summary import SchedulingSummary
from esinos.ui.report import render_scheduling_report
from esinos.ui.process_input import (
    read_processes,
    _read_integer,
)


def run_custom_scheduling(
    *,
    input_fn: Callable[[str], str] = input,
    output_fn: Callable[[str], None] = print,
) -> None:
    """
    Run an interactive custom scheduling session.

    Processes are entered once and reused across algorithms.
    """

    try:
        # Step 1: Create the processes
        processes = read_processes(
            input_fn=input_fn,
            output_fn=output_fn,
        )

        # Step 2: Keep the session active
        while True:
            output_fn("\nESINOS - CUSTOM SCHEDULING")
            output_fn("[1] FCFS")
            output_fn("[2] SJF")
            output_fn("[3] Round Robin")
            output_fn("[4] Priority Scheduling")
            output_fn("[5] Compare all four algorithms")
            output_fn("[0] Back to Main Menu")

            choice = input_fn(
                "Select an algorithm: "
            ).strip()

            if choice == "0":
                output_fn("Returning to main menu.")
                return

            if choice not in ("1", "2", "3", "4", "5"):
                output_fn(
                    "Invalid option. Please try again."
                )
                continue
            
            # Option 5: Compare all four scheduling algorithms
            if choice == "5":

                quantum = _read_integer(
                    "Comparison RR quantum [default 2]: ",
                    minimum=1,
                    default=2,
                    input_fn=input_fn,
                    output_fn=output_fn,
                )

                # Execute all algorithms on the same workload
                runs = (
                    schedule_fcfs(processes),
                    schedule_sjf(processes),
                    schedule_rr(processes, quantum),
                    schedule_priority(processes),
                )

                # Convert results to SchedulingSummary objects
                summaries = [
                    SchedulingSummary(
                        results=tuple(results),
                        gantt=tuple(gantt),
                    )
                    for results, gantt in runs
                ]

                # Produce the four-way report
                report = render_four_way_comparison(
                    *summaries,
                    quantum=quantum,
                )

                output_fn("\n" + report)

                # Return to the custom scheduling menu
                continue
                
            # Step 3: Execute the chosen algorithm
            if choice == "1":
                algorithm = "FCFS"
                results, gantt = schedule_fcfs(processes)

            elif choice == "2":
                algorithm = "SJF"
                results, gantt = schedule_sjf(processes)

            elif choice == "3":
                algorithm = "RR"

                quantum = _read_integer(
                    "RR quantum [default 3]: ",
                    minimum=1,
                    default=3,
                    input_fn=input_fn,
                    output_fn=output_fn,
                )

                results, gantt = schedule_rr(
                    processes,
                    quantum,
                )

                output_fn(f"Time quantum: {quantum}")

            else:
                algorithm = "PRIORITY"
                results, gantt = schedule_priority(
                    processes
                )

            # Step 4: Build the scheduling summary
            summary = SchedulingSummary(
                results=tuple(results),
                gantt=tuple(gantt),
            )

            # Step 5: Display the standard report
            report = render_scheduling_report(
                summary,
                algorithm,
            )

            output_fn("\n" + report)

    except (EOFError, KeyboardInterrupt):
        output_fn("\nReturning to main menu.")
        return
