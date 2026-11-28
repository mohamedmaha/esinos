from collections.abc import Sequence

from .process import Process

from .result import GanttSegment, ProcessResult


def _validate_priority_inputs(
    processes: Sequence[Process],
) -> None:
    """Validate Priority Scheduling inputs."""

    # Step 1: Validate the process collection
    if not isinstance(processes, Sequence) or isinstance(
        processes, (str, bytes)
    ):
        raise TypeError("processes must be a sequence")

    if len(processes) == 0:
        raise ValueError("processes cannot be empty")

    # Step 2: Validate process objects and unique PIDs
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


def _select_highest_priority_ready(
    pending: Sequence[Process],
    current_time: int,
) -> Process | None:
    """
    Select the highest-priority ready process.

    Rules:
    - A process must have arrived.
    - Lower priority number means higher priority.
    - Earlier arrival wins when priorities are equal.
    - Original input order breaks remaining ties.

    Returns None if no process is ready.
    """

    ready = (
        process
        for process in pending
        if process.arrival_time <= current_time
    )

    return min(
        ready,
        key=lambda process: (
            process.priority,
            process.arrival_time,
        ),
        default=None,
    )


def schedule_priority(
    processes: Sequence[Process],
) -> tuple[list[ProcessResult], list[GanttSegment]]:
    """
    Schedule processes using non-preemptive Priority Scheduling.

    Rules:
    - Lower priority number means higher priority.
    - Only arrived processes can be selected.
    - Earlier arrival breaks priority ties.
    - Original input order breaks remaining ties.
    - Running processes cannot be preempted.
    """

    # Step 1: Validate processes
    _validate_priority_inputs(processes)

    # Step 2: Initialize simulation state
    pending = list(processes)

    results: list[ProcessResult] = []
    gantt: list[GanttSegment] = []

    current_time = 0

    # Step 3: Continue while processes remain
    while pending:

        selected = _select_highest_priority_ready(
            pending,
            current_time,
        )

        # Step 4: Handle CPU idle time
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

        # Step 5: Execute the selected process
        start_time = current_time

        current_time += selected.burst_time

        # Step 6: Record CPU execution
        gantt.append(
            GanttSegment(
                pid=selected.pid,
                start=start_time,
                end=current_time,
            )
        )

        # Step 7: Record final process results
        results.append(
            ProcessResult(
                process=selected,
                start_time=start_time,
                completion_time=current_time,
            )
        )

        # Step 8: Remove completed process
        pending.remove(selected)

    return results, gantt
