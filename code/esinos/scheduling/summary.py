from dataclasses import dataclass

from .result import GanttSegment, ProcessResult


@dataclass(frozen=True)
class SchedulingSummary:
    """
    Store and analyze a complete CPU scheduling simulation.

    Attributes:
        results: Individual process scheduling results.
        gantt: Chronological CPU execution and idle segments.
    """

    results: tuple[ProcessResult, ...]
    gantt: tuple[GanttSegment, ...]

    def __post_init__(self) -> None:
        # Step 1: Validate the collections
        if not isinstance(self.results, tuple):
            raise TypeError("results must be a tuple")

        if not isinstance(self.gantt, tuple):
            raise TypeError("gantt must be a tuple")

        if not self.results or not self.gantt:
            raise ValueError("Scheduling data cannot be empty")

        if any(not isinstance(r, ProcessResult) for r in self.results):
            raise TypeError("Invalid process result")

        if any(not isinstance(g, GanttSegment) for g in self.gantt):
            raise TypeError("Invalid Gantt segment")

        # Step 2: Validate the Gantt timeline
        if self.gantt[0].start != 0:
            raise ValueError("Gantt timeline must start at 0")

        for i in range(1, len(self.gantt)):
            previous = self.gantt[i - 1]
            current = self.gantt[i]

            if current.start != previous.end:
                raise ValueError(
                    "Gantt segments must be continuous"
                )

        # Step 3: Validate process identifiers
        process_ids = [r.pid for r in self.results]

        if len(process_ids) != len(set(process_ids)):
            raise ValueError("Duplicate process results")

        # Step 4: Verify CPU execution durations
        cpu_durations = {pid: 0 for pid in process_ids}
        first_start = {}
        last_end = {}

        for segment in self.gantt:
            if segment.pid is None:
                continue

            if segment.pid not in cpu_durations:
                raise ValueError("Unknown process in Gantt")

            cpu_durations[segment.pid] += segment.duration
            first_start.setdefault(segment.pid, segment.start)
            last_end[segment.pid] = segment.end

        for result in self.results:
            pid = result.pid

            if cpu_durations[pid] != result.process.burst_time:
                raise ValueError(
                    f"CPU duration mismatch for {pid}"
                )

            if first_start.get(pid) != result.start_time:
                raise ValueError(
                    f"Start time mismatch for {pid}"
                )

            if last_end.get(pid) != result.completion_time:
                raise ValueError(
                    f"Completion time mismatch for {pid}"
                )

    @property
    def process_count(self) -> int:
        return len(self.results)

    @property
    def average_waiting_time(self) -> float:
        return sum(
            r.waiting_time for r in self.results
        ) / self.process_count

    @property
    def average_turnaround_time(self) -> float:
        return sum(
            r.turnaround_time for r in self.results
        ) / self.process_count

    @property
    def average_response_time(self) -> float:
        return sum(
            r.response_time for r in self.results
        ) / self.process_count

    @property
    def cpu_busy_time(self) -> int:
        return sum(
            segment.duration
            for segment in self.gantt
            if segment.pid is not None
        )

    @property
    def cpu_idle_time(self) -> int:
        return sum(
            segment.duration
            for segment in self.gantt
            if segment.pid is None
        )

    @property
    def makespan(self) -> int:
        return self.gantt[-1].end

    @property
    def cpu_utilization(self) -> float:
        return (self.cpu_busy_time / self.makespan) * 100
