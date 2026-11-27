import random

import pytest

from esinos.scheduling.process import Process
from esinos.scheduling.fcfs import schedule_fcfs
from esinos.scheduling.sjf import schedule_sjf
from esinos.scheduling.summary import SchedulingSummary


def make_summary(results, gantt):
    return SchedulingSummary(
        results=tuple(results),
        gantt=tuple(gantt),
    )


def reference_sjf(processes):
    """
    Build the expected SJF timeline independently
    for comparison with the production scheduler.
    """
    remaining = list(enumerate(processes))
    clock = 0

    expected_results = []
    expected_gantt = []

    while remaining:
        ready = [
            (index, process)
            for index, process in remaining
            if process.arrival_time <= clock
        ]

        if not ready:
            next_arrival = min(
                p.arrival_time for _, p in remaining
            )
            expected_gantt.append(
                ("IDLE", clock, next_arrival)
            )
            clock = next_arrival
            continue

        index, process = min(
            ready,
            key=lambda item: (
                item[1].burst_time,
                item[1].arrival_time,
                item[0],
            ),
        )

        finish = clock + process.burst_time

        expected_results.append(
            (process.pid, clock, finish)
        )
        expected_gantt.append(
            (process.pid, clock, finish)
        )

        remaining.remove((index, process))
        clock = finish

    return expected_results, expected_gantt


def test_sjf_randomized_scenarios():
    """Audit 100 reproducible scheduling scenarios."""

    rng = random.Random(2026)

    for _ in range(100):
        count = rng.randint(1, 12)

        processes = [
            Process(
                f"P{i}",
                rng.randint(0, 40),
                rng.randint(1, 12),
            )
            for i in range(count)
        ]

        original = list(processes)

        results, gantt = schedule_sjf(processes)
        summary = make_summary(results, gantt)

        expected_results, expected_gantt = reference_sjf(
            processes
        )

        actual_results = [
            (r.pid, r.start_time, r.completion_time)
            for r in results
        ]

        actual_gantt = [
            (g.label, g.start, g.end)
            for g in gantt
        ]

        assert actual_results == expected_results
        assert actual_gantt == expected_gantt

        assert len(results) == count
        assert summary.cpu_busy_time == sum(
            p.burst_time for p in processes
        )

        assert (
            summary.cpu_busy_time + summary.cpu_idle_time
            == summary.makespan
        )

        for result in results:
            assert result.start_time >= result.process.arrival_time
            assert result.completion_time == (
                result.start_time + result.process.burst_time
            )
            assert result.waiting_time >= 0
            assert result.response_time == result.waiting_time

        assert processes == original


def test_sjf_optimal_for_simultaneous_arrivals():
    """SJF average waiting time is no worse than FCFS."""

    rng = random.Random(1234)

    for _ in range(50):
        count = rng.randint(2, 10)

        processes = [
            Process(f"P{i}", 0, rng.randint(1, 20))
            for i in range(count)
        ]

        fcfs_results, fcfs_gantt = schedule_fcfs(processes)
        sjf_results, sjf_gantt = schedule_sjf(processes)

        fcfs = make_summary(fcfs_results, fcfs_gantt)
        sjf = make_summary(sjf_results, sjf_gantt)

        assert (
            sjf.average_waiting_time
            <= fcfs.average_waiting_time
        )

        assert sjf.cpu_busy_time == fcfs.cpu_busy_time

        sjf_bursts = [
            r.process.burst_time for r in sjf_results
        ]

        assert sjf_bursts == sorted(sjf_bursts)


def test_sjf_multiple_idle_intervals_and_ties():
    processes = [
        Process("P2", 4, 2),
        Process("P1", 4, 2),
        Process("P3", 9, 1),
        Process("P4", 17, 3),
    ]

    results, gantt = schedule_sjf(processes)
    summary = make_summary(results, gantt)

    assert [r.pid for r in results] == [
        "P2", "P1", "P3", "P4"
    ]

    assert [
        (g.label, g.start, g.end)
        for g in gantt
    ] == [
        ("IDLE", 0, 4),
        ("P2", 4, 6),
        ("P1", 6, 8),
        ("IDLE", 8, 9),
        ("P3", 9, 10),
        ("IDLE", 10, 17),
        ("P4", 17, 20),
    ]

    assert summary.cpu_busy_time == 8
    assert summary.cpu_idle_time == 12
    assert summary.makespan == 20
    assert summary.cpu_utilization == pytest.approx(40)


def test_sjf_does_not_preempt_running_process():
    processes = [
        Process("P1", 0, 15),
        Process("P2", 1, 1),
        Process("P3", 2, 2),
    ]

    results, gantt = schedule_sjf(processes)

    assert [r.pid for r in results] == [
        "P1", "P2", "P3"
    ]

    assert [
        (g.start, g.end) for g in gantt
    ] == [
        (0, 15),
        (15, 16),
        (16, 18),
    ]

    assert results[1].waiting_time == 14
    assert results[2].waiting_time == 14


def test_sjf_handles_large_time_values():
    processes = [
        Process("P1", 1_000_000, 3),
        Process("P2", 1_000_001, 1),
        Process("P3", 1_000_002, 2),
    ]

    results, gantt = schedule_sjf(processes)
    summary = make_summary(results, gantt)

    assert [
        (g.label, g.start, g.end)
        for g in gantt
    ] == [
        ("IDLE", 0, 1_000_000),
        ("P1", 1_000_000, 1_000_003),
        ("P2", 1_000_003, 1_000_004),
        ("P3", 1_000_004, 1_000_006),
    ]

    assert summary.cpu_busy_time == 6
    assert summary.cpu_idle_time == 1_000_000
    assert summary.makespan == 1_000_006

    assert summary.cpu_utilization == pytest.approx(
        6 / 1_000_006 * 100
    )
