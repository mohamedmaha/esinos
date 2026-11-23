import random

from esinos.scheduling.process import Process
from esinos.scheduling.fcfs import schedule_fcfs
from esinos.scheduling.summary import SchedulingSummary


def test_fcfs_random_scenarios():
    """Verify FCFS invariants over 100 reproducible scenarios."""

    rng = random.Random(2026)

    for _ in range(100):
        count = rng.randint(1, 12)

        processes = [
            Process(
                pid=f"P{i}",
                arrival_time=rng.randint(0, 30),
                burst_time=rng.randint(1, 15),
            )
            for i in range(count)
        ]

        original = list(processes)

        results, gantt = schedule_fcfs(processes)

        summary = SchedulingSummary(
            tuple(results),
            tuple(gantt),
        )

        expected_order = sorted(
            processes,
            key=lambda p: p.arrival_time,
        )

        assert [r.process for r in results] == expected_order

        clock = 0

        for result in results:
            expected_start = max(
                clock,
                result.process.arrival_time,
            )

            assert result.start_time == expected_start

            assert result.completion_time == (
                expected_start + result.process.burst_time
            )

            assert result.waiting_time >= 0
            assert result.response_time == result.waiting_time

            clock = result.completion_time

        assert summary.makespan == clock

        assert summary.cpu_busy_time == sum(
            p.burst_time for p in processes
        )

        assert (
            summary.cpu_busy_time + summary.cpu_idle_time
            == summary.makespan
        )

        assert processes == original


def test_fcfs_long_idle_intervals():
    """Verify that long idle periods appear in the Gantt chart."""

    processes = [
        Process("P1", 3, 2),
        Process("P2", 10, 1),
    ]

    _, gantt = schedule_fcfs(processes)

    actual = [
        (segment.label, segment.start, segment.end)
        for segment in gantt
    ]

    assert actual == [
        ("IDLE", 0, 3),
        ("P1", 3, 5),
        ("IDLE", 5, 10),
        ("P2", 10, 11),
    ]


def test_fcfs_is_non_preemptive():
    """A short process cannot interrupt a running FCFS process."""

    processes = [
        Process("P1", 0, 9),
        Process("P2", 1, 1),
    ]

    results, gantt = schedule_fcfs(processes)

    assert results[0].completion_time == 9
    assert results[1].start_time == 9
    assert results[1].waiting_time == 8

    assert [segment.label for segment in gantt] == [
        "P1",
        "P2",
    ]
