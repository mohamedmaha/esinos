from collections import deque
from collections.abc import Sequence

from .result import GanttSegment, ProcessResult


from .process import Process


def _validate_rr_inputs(
    processes: Sequence[Process],
    quantum: int,
) -> None:
    """Validate Round Robin scheduling inputs."""

    # Step 1: Validate the collection
    if not isinstance(processes, Sequence) or isinstance(
        processes, (str, bytes)
    ):
        raise TypeError("processes must be a sequence")

    if len(processes) == 0:
        raise ValueError("processes cannot be empty")

    # Step 2: Validate each process and its PID
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

    # Step 3: Validate the quantum
    if type(quantum) is not int:
        raise TypeError("quantum must be an integer")

    if quantum <= 0:
        raise ValueError("quantum must be positive")


def _enqueue_arrivals(
    ordered: Sequence[Process],
    next_index: int,
    current_time: int,
    ready: deque[Process],
) -> int:
    """
    Enqueue processes that have arrived.

    Preconditions:
    - ordered is sorted by arrival time (stable order)
    - next_index points to the first not-yet-enqueued process

    Returns the updated next_index.
    """

    while (
        next_index < len(ordered)
        and ordered[next_index].arrival_time <= current_time
    ):
        ready.append(ordered[next_index])
        next_index += 1

    return next_index


def schedule_rr(
    processes: Sequence[Process],
    quantum: int,
) -> tuple[list[ProcessResult], list[GanttSegment]]:
    """
    Schedule processes using preemptive Round Robin.

    Arrivals at a quantum boundary are enqueued
    before the interrupted process is requeued.

    Context-switch overhead is assumed to be zero.
    """

    # Step 1: Validate inputs
    _validate_rr_inputs(processes, quantum)

    # Step 2: Sort processes by arrival time
    ordered = sorted(
        processes,
        key=lambda process: process.arrival_time,
    )

    # Step 3: Initialize simulation state
    ready: deque[Process] = deque()

    remaining_time = {
        process.pid: process.burst_time
        for process in ordered
    }

    first_start_time: dict[str, int] = {}

    results: list[ProcessResult] = []
    gantt: list[GanttSegment] = []

    current_time = 0
    next_index = 0

    # Step 4: Continue until all processes finish
    while len(results) < len(ordered):

        next_index = _enqueue_arrivals(
            ordered,
            next_index,
            current_time,
            ready,
        )

        # Step 5: Handle CPU idle intervals
        if not ready:
            next_arrival = ordered[next_index].arrival_time

            gantt.append(
                GanttSegment(
                    pid=None,
                    start=current_time,
                    end=next_arrival,
                )
            )

            current_time = next_arrival
            continue

        # Step 6: Select first ready process
        process = ready.popleft()

        pid = process.pid

        # Remember the FIRST execution only
        if pid not in first_start_time:
            first_start_time[pid] = current_time

        # Step 7: Execute at most one quantum
        execution_time = min(
            quantum,
            remaining_time[pid],
        )

        start = current_time
        current_time += execution_time

        remaining_time[pid] -= execution_time

        # Step 8: Record CPU execution
        gantt.append(
            GanttSegment(
                pid=pid,
                start=start,
                end=current_time,
            )
        )

        # Step 9: Enqueue newly arrived processes
        next_index = _enqueue_arrivals(
            ordered,
            next_index,
            current_time,
            ready,
        )

        # Step 10: Finish or requeue the process
        if remaining_time[pid] == 0:
            results.append(
                ProcessResult(
                    process=process,
                    start_time=first_start_time[pid],
                    completion_time=current_time,
                )
            )
        else:
            ready.append(process)

    return results, gantt
