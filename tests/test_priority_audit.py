import random

from esinos.scheduling.process import Process
from esinos.scheduling.fcfs import schedule_fcfs
from esinos.scheduling.priority import schedule_priority
from esinos.scheduling.summary import SchedulingSummary


def timeline(gantt):
    """Convert Gantt segments to comparable tuples."""
    return [
        (segment.label, segment.start, segment.end)
        for segment in gantt
    ]


def reference_priority(processes):
    """
    Independent non-preemptive Priority simulation.

    Selection rules:
    - Lower priority number wins.
    - Earlier arrival breaks priority ties.
    - Input order breaks remaining ties.
    """

    waiting = set(range(len(processes)))

    clock = 0
    expected_results = {}
    expected_gantt = []

    while waiting:

        # Step 1: Find processes ready at current time
        ready_indices = [
            index
            for index in waiting
            if processes[index].arrival_time <= clock
        ]

        # Step 2: Handle an idle CPU
        if not ready_indices:
            next_arrival = min(
                processes[index].arrival_time
                for index in waiting
            )

            expected_gantt.append(
                ("IDLE", clock, next_arrival)
            )

            clock = next_arrival
            continue

        # Step 3: Select the highest-priority process
        selected_index = min(
            ready_indices,
            key=lambda index: (
                processes[index].priority,
                processes[index].arrival_time,
                index,
            ),
        )

        process = processes[selected_index]

        start = clock

        # Step 4: Simulate execution one unit at a time
        for _ in range(process.burst_time):
            clock += 1

        # Step 5: Record completion
        expected_gantt.append(
            (process.pid, start, clock)
        )

        expected_results[process.pid] = (
            start,
            clock,
        )

        waiting.remove(selected_index)

    return expected_results, expected_gantt


def test_priority_randomized_reference_audit():
    """Audit 100 deterministic scheduling scenarios."""

    rng = random.Random(2026)

    for scenario in range(100):

        count = rng.randint(1, 10)

        processes = [
            Process(
                pid=f"P{i}",
                arrival_time=rng.randint(0, 30),
                burst_time=rng.randint(1, 12),
                priority=rng.randint(1, 6),
            )
            for i in range(count)
        ]

        rng.shuffle(processes)
        original = list(processes)

        # Actual ESINOS scheduler
        results, gantt = schedule_priority(processes)

        # Independent reference simulation
        expected_results, expected_gantt = (
            reference_priority(processes)
        )

        actual_results = {
            result.pid: (
                result.start_time,
                result.completion_time,
            )
            for result in results
        }

        assert actual_results == expected_results, (
            f"Scenario {scenario}"
        )

        assert timeline(gantt) == expected_gantt, (
            f"Scenario {scenario}"
        )

        # Verify process completion order
        assert [r.pid for r in results] == [
            label
            for label, _, _ in expected_gantt
            if label != "IDLE"
        ]

        summary = SchedulingSummary(
            tuple(results),
            tuple(gantt),
        )

        assert summary.process_count == count

        assert summary.cpu_busy_time == sum(
            process.burst_time for process in processes
        )

        assert (
            summary.cpu_busy_time
            + summary.cpu_idle_time
            == summary.makespan
        )

        for result in results:
            assert result.waiting_time >= 0
            assert result.turnaround_time >= 0

            # Non-preemptive scheduling
            assert (
                result.response_time
                == result.waiting_time
            )

        # Input must not be modified
        assert processes == original


def test_priority_equal_priorities_match_fcfs_randomized():
    """Check Priority/FCFS equivalence in 40 scenarios."""

    rng = random.Random(2027)

    for _ in range(40):

        count = rng.randint(1, 10)

        processes = [
            Process(
                pid=f"P{i}",
                arrival_time=rng.randint(0, 30),
                burst_time=rng.randint(1, 12),
                priority=1,
            )
            for i in range(count)
        ]

        rng.shuffle(processes)

        priority_results, priority_gantt = (
            schedule_priority(processes)
        )

        fcfs_results, fcfs_gantt = (
            schedule_fcfs(processes)
        )

        assert timeline(priority_gantt) == timeline(
            fcfs_gantt
        )

        assert [
            (
                result.pid,
                result.start_time,
                result.completion_time,
            )
            for result in priority_results
        ] == [
            (
                result.pid,
                result.start_time,
                result.completion_time,
            )
            for result in fcfs_results
        ]


def test_priority_no_preemption_on_new_arrival():
    processes = [
        Process("P1", 0, 8, priority=5),
        Process("P2", 2, 1, priority=1),
        Process("P3", 3, 1, priority=2),
    ]

    _, gantt = schedule_priority(processes)

    assert timeline(gantt) == [
        ("P1", 0, 8),
        ("P2", 8, 9),
        ("P3", 9, 10),
    ]


def test_priority_deterministic_tie_breaking():
    processes = [
        Process("P4", 4, 1, priority=2),
        Process("P2", 2, 2, priority=1),
        Process("P3", 2, 1, priority=1),
        Process("P1", 0, 5, priority=3),
    ]

    _, gantt = schedule_priority(processes)

    assert timeline(gantt) == [
        ("P1", 0, 5),
        ("P2", 5, 7),
        ("P3", 7, 8),
        ("P4", 8, 9),
    ]


def test_priority_large_arrivals_and_idle_intervals():
    processes = [
        Process("P1", 1_000_000, 3, priority=3),
        Process("P2", 1_000_001, 1, priority=1),
        Process("P3", 1_000_010, 2, priority=2),
    ]

    results, gantt = schedule_priority(processes)

    assert timeline(gantt) == [
        ("IDLE", 0, 1_000_000),
        ("P1", 1_000_000, 1_000_003),
        ("P2", 1_000_003, 1_000_004),
        ("IDLE", 1_000_004, 1_000_010),
        ("P3", 1_000_010, 1_000_012),
    ]

    summary = SchedulingSummary(
        tuple(results),
        tuple(gantt),
    )

    assert summary.cpu_busy_time == 6
    assert summary.cpu_idle_time == 1_000_006
    assert summary.makespan == 1_000_012


def test_priority_low_priority_waiting_risk():
    """
    Demonstrate long waiting for low-priority work.

    This is a finite starvation-risk example,
    not proof of infinite starvation.
    """

    processes = [
        Process("LOW", 0, 1, priority=9),
        Process("H1", 0, 3, priority=1),
        Process("H2", 1, 2, priority=1),
        Process("H3", 2, 2, priority=1),
    ]

    results, gantt = schedule_priority(processes)

    assert timeline(gantt) == [
        ("H1", 0, 3),
        ("H2", 3, 5),
        ("H3", 5, 7),
        ("LOW", 7, 8),
    ]

    by_pid = {
        result.pid: result
        for result in results
    }

    assert by_pid["LOW"].waiting_time == 7
    assert by_pid["H1"].waiting_time == 0
