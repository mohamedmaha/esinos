import random
from collections import deque

import pytest

from esinos.scheduling.process import Process
from esinos.scheduling.fcfs import schedule_fcfs
from esinos.scheduling.rr import schedule_rr
from esinos.scheduling.summary import SchedulingSummary


def timeline(gantt):
    return [
        (segment.label, segment.start, segment.end)
        for segment in gantt
    ]


def make_summary(results, gantt):
    return SchedulingSummary(
        results=tuple(results),
        gantt=tuple(gantt),
    )


def reference_rr(processes, quantum):
    """
    Reference RR simulation using one-unit CPU steps.

    This is a test oracle, independent of schedule_rr().
    """

    ordered = sorted(
        enumerate(processes),
        key=lambda item: (
            item[1].arrival_time,
            item[0],
        ),
    )

    ready = deque()

    remaining = {
        p.pid: p.burst_time
        for p in processes
    }

    first_start = {}
    completion = {}
    expected_gantt = []

    clock = 0
    next_index = 0

    while len(completion) < len(ordered):

        # Add arrivals known at the current instant
        while (
            next_index < len(ordered)
            and ordered[next_index][1].arrival_time <= clock
        ):
            ready.append(ordered[next_index][1])
            next_index += 1

        if not ready:
            next_arrival = (
                ordered[next_index][1].arrival_time
            )

            expected_gantt.append(
                ("IDLE", clock, next_arrival)
            )

            clock = next_arrival
            continue

        process = ready.popleft()
        pid = process.pid

        if pid not in first_start:
            first_start[pid] = clock

        start = clock
        used = 0

        # Simulate one CPU unit at a time
        while used < quantum and remaining[pid] > 0:
            clock += 1
            used += 1
            remaining[pid] -= 1

            # Include arrivals at the quantum boundary
            while (
                next_index < len(ordered)
                and ordered[next_index][1].arrival_time <= clock
            ):
                ready.append(ordered[next_index][1])
                next_index += 1

        expected_gantt.append(
            (pid, start, clock)
        )

        if remaining[pid] == 0:
            completion[pid] = clock
        else:
            ready.append(process)

    expected_results = {
        pid: (first_start[pid], completion[pid])
        for pid in completion
    }

    return expected_results, expected_gantt


def test_rr_randomized_reference_audit():
    """Compare 100 reproducible RR scenarios."""

    rng = random.Random(2026)

    for _ in range(100):
        count = rng.randint(1, 10)
        quantum = rng.randint(1, 7)

        processes = [
            Process(
                f"P{i}",
                rng.randint(0, 25),
                rng.randint(1, 12),
            )
            for i in range(count)
        ]

        original = list(processes)

        results, gantt = schedule_rr(
            processes,
            quantum,
        )

        expected_results, expected_gantt = reference_rr(
            processes,
            quantum,
        )

        actual_results = {
            r.pid: (
                r.start_time,
                r.completion_time,
            )
            for r in results
        }

        assert actual_results == expected_results
        assert timeline(gantt) == expected_gantt

        summary = make_summary(results, gantt)

        assert summary.process_count == count
        assert summary.cpu_busy_time == sum(
            p.burst_time for p in processes
        )

        assert (
            summary.cpu_busy_time + summary.cpu_idle_time
            == summary.makespan
        )

        for result in results:
            assert result.waiting_time >= 0
            assert result.response_time >= 0
            assert result.response_time <= result.waiting_time

        assert processes == original


def test_rr_large_quantum_matches_fcfs_randomized():
    """RR behaves as FCFS when each burst fits in one quantum."""

    rng = random.Random(2027)

    for _ in range(40):
        count = rng.randint(1, 9)

        processes = [
            Process(
                f"P{i}",
                rng.randint(0, 20),
                rng.randint(1, 12),
            )
            for i in range(count)
        ]

        quantum = max(
            p.burst_time for p in processes
        )

        fcfs_results, fcfs_gantt = schedule_fcfs(
            processes
        )

        rr_results, rr_gantt = schedule_rr(
            processes,
            quantum,
        )

        assert timeline(rr_gantt) == timeline(fcfs_gantt)

        assert [
            (r.pid, r.start_time, r.completion_time)
            for r in rr_results
        ] == [
            (r.pid, r.start_time, r.completion_time)
            for r in fcfs_results
        ]


def test_rr_multiple_arrivals_at_boundary():
    processes = [
        Process("P1", 0, 5),
        Process("P2", 1, 1),
        Process("P3", 2, 1),
        Process("P4", 2, 2),
    ]

    _, gantt = schedule_rr(processes, 2)

    assert timeline(gantt) == [
        ("P1", 0, 2),
        ("P2", 2, 3),
        ("P3", 3, 4),
        ("P4", 4, 6),
        ("P1", 6, 8),
        ("P1", 8, 9),
    ]


def test_rr_idle_before_and_between_processes():
    processes = [
        Process("P1", 5, 4),
        Process("P2", 6, 1),
        Process("P3", 20, 2),
    ]

    results, gantt = schedule_rr(processes, 2)

    assert timeline(gantt) == [
        ("IDLE", 0, 5),
        ("P1", 5, 7),
        ("P2", 7, 8),
        ("P1", 8, 10),
        ("IDLE", 10, 20),
        ("P3", 20, 22),
    ]

    summary = make_summary(results, gantt)

    assert summary.cpu_busy_time == 7
    assert summary.cpu_idle_time == 15
    assert summary.makespan == 22


def test_rr_response_and_waiting_are_distinct():
    processes = [
        Process("P1", 0, 5),
        Process("P2", 0, 1),
    ]

    results, gantt = schedule_rr(processes, 2)

    by_pid = {r.pid: r for r in results}

    assert by_pid["P1"].response_time == 0
    assert by_pid["P1"].waiting_time == 1

    assert by_pid["P2"].response_time == 2
    assert by_pid["P2"].waiting_time == 2

    summary = make_summary(results, gantt)

    assert summary.average_response_time == pytest.approx(1)
    assert summary.average_waiting_time == pytest.approx(1.5)


def test_rr_large_arrival_time():
    processes = [
        Process("P1", 1_000_000, 3),
        Process("P2", 1_000_001, 1),
    ]

    results, gantt = schedule_rr(processes, 2)

    assert timeline(gantt) == [
        ("IDLE", 0, 1_000_000),
        ("P1", 1_000_000, 1_000_002),
        ("P2", 1_000_002, 1_000_003),
        ("P1", 1_000_003, 1_000_004),
    ]

    summary = make_summary(results, gantt)

    assert summary.cpu_busy_time == 4
    assert summary.cpu_idle_time == 1_000_000
    assert summary.makespan == 1_000_004
