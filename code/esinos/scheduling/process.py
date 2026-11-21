from dataclasses import dataclass


@dataclass(frozen=True)
class Process:
    """
    Represent a process in the ESINOS simulator.

    Attributes:
        pid: Unique process identifier.
        arrival_time: Arrival time in the system.
        burst_time: Required CPU execution time.
        priority: Scheduling priority (1 = highest).
    """

    pid: str
    arrival_time: int
    burst_time: int
    priority: int = 1

    def __post_init__(self) -> None:
        if not isinstance(self.pid, str) or not self.pid.strip():
            raise ValueError("pid must be a non-empty string")

        if type(self.arrival_time) is not int or self.arrival_time < 0:
            raise ValueError(
                "arrival_time must be a non-negative integer"
            )

        if type(self.burst_time) is not int or self.burst_time <= 0:
            raise ValueError(
                "burst_time must be a positive integer"
            )

        if type(self.priority) is not int or self.priority < 1:
            raise ValueError(
                "priority must be a positive integer"
            )
