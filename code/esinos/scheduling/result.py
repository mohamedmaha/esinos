from .process import Process

from dataclasses import dataclass


@dataclass(frozen=True)
class GanttSegment:
    """
    Represent one CPU execution or idle interval.

    Attributes:
        pid: Process identifier, or None for IDLE.
        start: Starting time.
        end: Ending time.
    """

    pid: str | None
    start: int
    end: int

    def __post_init__(self) -> None:
        if self.pid is not None:
            if not isinstance(self.pid, str) or not self.pid.strip():
                raise ValueError("pid must be a non-empty string or None")

        if type(self.start) is not int or self.start < 0:
            raise ValueError("start must be a non-negative integer")

        if type(self.end) is not int or self.end <= self.start:
            raise ValueError("end must be greater than start")

    @property
    def duration(self) -> int:
        return self.end - self.start

    @property
    def label(self) -> str:
        return self.pid if self.pid is not None else "IDLE"


@dataclass(frozen=True)
class ProcessResult:
    """
    Store the scheduling result of a process.

    Attributes:
        process: Original process data.
        start_time: First CPU execution time.
        completion_time: Process completion time.
    """

    process: Process
    start_time: int
    completion_time: int

    def __post_init__(self) -> None:
        if not isinstance(self.process, Process):
            raise TypeError("process must be a Process instance")

        if type(self.start_time) is not int:
            raise ValueError("start_time must be an integer")

        if type(self.completion_time) is not int:
            raise ValueError("completion_time must be an integer")

        if self.start_time < self.process.arrival_time:
            raise ValueError(
                "start_time cannot be before arrival_time"
            )

        if self.completion_time < (
            self.start_time + self.process.burst_time
        ):
            raise ValueError(
                "completion_time is too early for the CPU burst"
            )

    @property
    def pid(self) -> str:
        return self.process.pid

    @property
    def turnaround_time(self) -> int:
        return self.completion_time - self.process.arrival_time

    @property
    def waiting_time(self) -> int:
        return self.turnaround_time - self.process.burst_time

    @property
    def response_time(self) -> int:
        return self.start_time - self.process.arrival_time
