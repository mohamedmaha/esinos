import pytest

from esinos.scheduling.process import Process
from esinos.scheduling.fcfs import schedule_fcfs
from esinos.scheduling.priority import schedule_priority
from esinos.scheduling.summary import SchedulingSummary
from esinos.ui.report import render_scheduling_report


def get_timeline(gantt):
    return [
        (segment.label, segment.start, segment.end)
        for segment in gantt
    ]


def reference_processes():
    return [
        Process("P1", 0, 6, priority=3),
        Process("P2", 1, 2, priority=1),
        Process("P3", 2, 4, priority=2),
        Process("P4", 4, 1, priority=1),
    ]


def test_priority_reference_scenario():
    processes = reference_processes()

    results, gantt = schedule_priority(processes)

    assert get_timeline(gantt) == [
        ("P1", 0, 6),
        ("P2", 6, 8),
        ("P4", 8, 9),
        ("P3", 9, 13),
    ]

    assert [result.pid for result in results] == [
        "P1", "P2", "P4", "P3"
    ]


def test_priority_reference_metrics_and_report():
    results, gantt = schedule_priority(
        reference_processes()
    )

    by_pid = {result.pid: result for result in results}

    assert by_pid["P1"].waiting_time == 0
    assert by_pid["P2"].waiting_time == 5
    assert by_pid["P3"].waiting_time == 7
    assert by_pid["P4"].waiting_time == 4

    summary = SchedulingSummary(
        tuple(results),
        tuple(gantt),
    )

    assert summary.average_waiting_time == pytest.approx(4)
    assert summary.average_turnaround_time == pytest.approx(
        7.25
    )
    assert summary.average_response_time == pytest.approx(4)

    assert summary.cpu_busy_time == 13
    assert summary.cpu_idle_time == 0
    assert summary.makespan == 13
    assert summary.cpu_utilization == pytest.approx(100)

    report = render_scheduling_report(
        summary,
        "PRIORITY",
    )

    assert "CPU SCHEDULING | PRIORITY" in report
    assert "PROCESS RESULTS" in report
    assert "CPU GANTT" in report
    assert "SCHEDULING SUMMARY" in report


def test_priority_is_non_preemptive():
    processes = [
        Process("P1", 0, 6, priority=4),
        Process("P2", 1, 1, priority=1),
    ]

    _, gantt = schedule_priority(processes)

    assert get_timeline(gantt) == [
        ("P1", 0, 6),
        ("P2", 6, 7),
    ]


def test_priority_beats_shorter_burst():
    processes = [
        Process("P1", 0, 1, priority=3),
        Process("P2", 0, 5, priority=1),
    ]

    _, gantt = schedule_priority(processes)

    assert get_timeline(gantt) == [
        ("P2", 0, 5),
        ("P1", 5, 6),
    ]


def test_priority_tie_uses_earlier_arrival():
    processes = [
        Process("P1", 0, 3, priority=3),
        Process("P2", 2, 1, priority=1),
        Process("P3", 1, 1, priority=1),
    ]

    _, gantt = schedule_priority(processes)

    assert get_timeline(gantt) == [
        ("P1", 0, 3),
        ("P3", 3, 4),
        ("P2", 4, 5),
    ]


def test_priority_tie_preserves_input_order():
    processes = [
        Process("P2", 0, 2, priority=1),
        Process("P1", 0, 1, priority=1),
        Process("P3", 0, 1, priority=2),
    ]

    _, gantt = schedule_priority(processes)

    assert get_timeline(gantt) == [
        ("P2", 0, 2),
        ("P1", 2, 3),
        ("P3", 3, 4),
    ]


def test_priority_handles_initial_idle():
    processes = [
        Process("P1", 4, 2, priority=2),
        Process("P2", 5, 1, priority=1),
    ]

    _, gantt = schedule_priority(processes)

    assert get_timeline(gantt) == [
        ("IDLE", 0, 4),
        ("P1", 4, 6),
        ("P2", 6, 7),
    ]


def test_priority_handles_idle_between_processes():
    processes = [
        Process("P1", 0, 1, priority=2),
        Process("P2", 5, 2, priority=1),
    ]

    results, gantt = schedule_priority(processes)

    assert get_timeline(gantt) == [
        ("P1", 0, 1),
        ("IDLE", 1, 5),
        ("P2", 5, 7),
    ]

    summary = SchedulingSummary(
        tuple(results),
        tuple(gantt),
    )

    assert summary.cpu_busy_time == 3
    assert summary.cpu_idle_time == 4
    assert summary.makespan == 7


def test_priority_equal_priorities_match_fcfs():
    processes = [
        Process("P3", 2, 1, priority=1),
        Process("P2", 0, 3, priority=1),
        Process("P1", 0, 2, priority=1),
    ]

    original = list(processes)

    priority_results, priority_gantt = schedule_priority(
        processes
    )

    fcfs_results, fcfs_gantt = schedule_fcfs(processes)

    assert get_timeline(priority_gantt) == get_timeline(
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

    assert processes == original


def test_priority_rejects_invalid_inputs():
    with pytest.raises(ValueError):
        schedule_priority([])

    with pytest.raises(TypeError):
        schedule_priority(None)

    with pytest.raises(TypeError):
        schedule_priority("P1")

    with pytest.raises(TypeError):
        schedule_priority([
            Process("P1", 0, 3),
            "invalid",
        ])

    with pytest.raises(ValueError):
        schedule_priority([
            Process("P1", 0, 3),
            Process("P1", 1, 2),
        ])
