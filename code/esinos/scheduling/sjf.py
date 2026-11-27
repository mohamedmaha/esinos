from collections.abc import Sequence

from .result import GanttSegment, ProcessResult

from .process import Process


def _validate_processes(
    processes: Sequence[Process],
) -> None:
    """Validate the input processes for SJF scheduling."""

    if not isinstance(processes, Sequence) or isinstance(
        processes, (str, bytes)
    ):
        raise TypeError("processes must be a sequence")

    if len(processes) == 0:
        raise ValueError("processes cannot be empty")

    seen_pids = set()

    for process in processes:
        if not isinstance(process, Process):
            raise TypeError(
                "all elements must be Process objects"
            )

        if process.pid in seen_pids:
            raise ValueError(
                f"duplicate process ID: {process.pid}"
            )

        seen_pids.add(process.pid)


def _select_shortest_ready(
    pending: Sequence[Process],
    current_time: int,
) -> Process | None:
    """
    Select the shortest ready process.

    Tie-breaking:
    1. Shortest burst time
    2. Earliest arrival time
    3. Original order in pending

    Return None if no process is ready.
    """

    ready = [
        process
        for process in pending
        if process.arrival_time <= current_time
    ]

    if not ready:
        return None

    return min(
        ready,
        key=lambda process: (
            process.burst_time,
            process.arrival_time,
        ),
    )


def schedule_sjf(
    processes: Sequence[Process],
) -> tuple[list[ProcessResult], list[GanttSegment]]:
    """
    Schedule processes using non-preemptive SJF.

    The shortest ready process is selected at each
    scheduling decision.

    Returns:
        - List of ProcessResult
        - List of GanttSegment
    """

    # Step 1: Validate input
    _validate_processes(processes)

    # Step 2: Initialize scheduling state
    pending = list(processes)

    results: list[ProcessResult] = []
    gantt: list[GanttSegment] = []

    current_time = 0

    # Step 3: Continue until all processes finish
    while pending:

        selected = _select_shortest_ready(
            pending,
            current_time,
        )

        # Step 4: CPU idle handling
        if selected is None:

            next_arrival = min(
                process.arrival_time
                for process in pending
            )

            gantt.append(
                GanttSegment(
                    pid=None,
                    start=current_time,
                    end=next_arrival,
                )
            )

            current_time = next_arrival
            continue

        # Step 5: Execute selected process
        start_time = current_time

        completion_time = (
            start_time + selected.burst_time
        )

        results.append(
            ProcessResult(
                process=selected,
                start_time=start_time,
                completion_time=completion_time,
            )
        )

        gantt.append(
            GanttSegment(
                pid=selected.pid,
                start=start_time,
                end=completion_time,
            )
        )

        # Step 6: Update CPU time
        current_time = completion_time

        # Step 7: Remove completed process
        pending.remove(selected)

    return results, gantt
