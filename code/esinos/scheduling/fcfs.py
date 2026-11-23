from collections.abc import Sequence

from .process import Process
from .result import GanttSegment, ProcessResult


def schedule_fcfs(
    processes: Sequence[Process],
) -> tuple[list[ProcessResult], list[GanttSegment]]:
    """
    Simulate First Come, First Served CPU scheduling.

    Processes are executed in arrival order.
    Equal arrival times preserve the original input order.

    Returns:
        A tuple containing:
        - Individual scheduling results
        - Gantt chart segments
    """

    # Step 1: Validate input
    if not processes:
        raise ValueError("At least one process is required")

    seen_pids = set()

    for process in processes:
        if not isinstance(process, Process):
            raise TypeError("All items must be Process instances")

        if process.pid in seen_pids:
            raise ValueError(
                f"Duplicate process identifier: {process.pid}"
            )

        seen_pids.add(process.pid)

    # Step 2: Sort processes by arrival time
    ordered_processes = sorted(
        processes,
        key=lambda process: process.arrival_time,
    )

    # Step 3: Initialize simulation state
    current_time = 0
    results: list[ProcessResult] = []
    gantt: list[GanttSegment] = []

    # Step 4: Execute each process
    for process in ordered_processes:

        # CPU is idle until the next process arrives
        if current_time < process.arrival_time:
            gantt.append(
                GanttSegment(
                    pid=None,
                    start=current_time,
                    end=process.arrival_time,
                )
            )

            current_time = process.arrival_time

        # Calculate execution interval
        start_time = current_time
        completion_time = start_time + process.burst_time

        # Store individual process results
        results.append(
            ProcessResult(
                process=process,
                start_time=start_time,
                completion_time=completion_time,
            )
        )

        # Store CPU execution segment
        gantt.append(
            GanttSegment(
                pid=process.pid,
                start=start_time,
                end=completion_time,
            )
        )

        # Advance simulation clock
        current_time = completion_time

    # Step 5: Return scheduling results
    return results, gantt
