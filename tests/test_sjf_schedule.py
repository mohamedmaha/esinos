import pytest

from esinos.scheduling.process import Process
from esinos.scheduling.sjf import schedule_sjf
from esinos.scheduling.summary import SchedulingSummary


def test_sjf_standard_scenario():
    processes = [
        Process("P1", 0, 7),
        Process("P2", 2, 4),
        Process("P3", 4, 1),
        Process("P4", 5, 4),
    ]

    results, gantt = schedule_sjf(processes)

    assert [r.pid for r in results] == [
        "P1", "P3", "P2", "P4"
    ]

    assert [
        (g.label, g.start, g.end)
        for g in gantt
    ] == [
        ("P1", 0, 7),
        ("P3", 7, 8),
        ("P2", 8, 12),
        ("P4", 12, 16),
    ]


def test_sjf_all_processes_arrive_at_zero():
    processes = [
        Process("P1", 0, 8),
        Process("P2", 0, 2),
        Process("P3", 0, 4),
    ]

    results, _ = schedule_sjf(processes)

    assert [r.pid for r in results] == [
        "P2", "P3", "P1"
    ]


def test_sjf_is_non_preemptive():
    processes = [
        Process("P1", 0, 9),
        Process("P2", 1, 1),
    ]

    results, _ = schedule_sjf(processes)

    assert results[0].pid == "P1"
    assert results[0].completion_time == 9
    assert results[1].start_time == 9
    assert results[1].waiting_time == 8


def test_sjf_handles_idle_intervals():
    processes = [
        Process("P1", 3, 2),
        Process("P2", 10, 1),
    ]

    _, gantt = schedule_sjf(processes)

    assert [
        (g.label, g.start, g.end)
        for g in gantt
    ] == [
        ("IDLE", 0, 3),
        ("P1", 3, 5),
        ("IDLE", 5, 10),
        ("P2", 10, 11),
    ]


def test_sjf_tie_breaking():
    processes = [
        Process("P0", 0, 5),
        Process("P1", 3, 2),
        Process("P2", 1, 2),
        Process("P3", 1, 2),
    ]

    results, _ = schedule_sjf(processes)

    assert [r.pid for r in results] == [
        "P0", "P2", "P3", "P1"
    ]


def test_sjf_includes_arrivals_at_current_time():
    processes = [
        Process("P1", 0, 4),
        Process("P2", 1, 3),
        Process("P3", 4, 1),
    ]

    results, _ = schedule_sjf(processes)

    assert [r.pid for r in results] == [
        "P1", "P3", "P2"
    ]


def test_sjf_invalid_inputs():
    with pytest.raises(ValueError):
        schedule_sjf([])

    with pytest.raises(TypeError):
        schedule_sjf(None)

    with pytest.raises(TypeError):
        schedule_sjf(["invalid"])

    with pytest.raises(ValueError):
        schedule_sjf([
            Process("P1", 0, 3),
            Process("P1", 1, 2),
        ])


def test_sjf_preserves_original_input():
    processes = [
        Process("P1", 0, 8),
        Process("P2", 0, 2),
    ]

    original = list(processes)

    schedule_sjf(processes)

    assert processes == original


def test_sjf_summary_compatibility():
    processes = [
        Process("P1", 2, 4),
        Process("P2", 3, 1),
        Process("P3", 8, 2),
    ]

    results, gantt = schedule_sjf(processes)

    summary = SchedulingSummary(
        results=tuple(results),
        gantt=tuple(gantt),
    )

    assert summary.process_count == 3
    assert summary.cpu_busy_time == 7
    assert summary.cpu_idle_time == 3
    assert summary.makespan == 10

    assert summary.average_waiting_time == pytest.approx(1)
    assert summary.average_turnaround_time == pytest.approx(10 / 3)
    assert summary.cpu_utilization == pytest.approx(70)
