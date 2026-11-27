import pytest

from esinos.scheduling.process import Process
from esinos.scheduling.fcfs import schedule_fcfs
from esinos.scheduling.rr import schedule_rr
from esinos.scheduling.summary import SchedulingSummary
from esinos.ui.report import render_scheduling_report


def get_timeline(gantt):
    return [
        (segment.label, segment.start, segment.end)
        for segment in gantt
    ]


def test_rr_reference_scenario():
    processes = [
        Process("P1", 0, 7),
        Process("P2", 2, 4),
        Process("P3", 3, 2),
    ]

    results, gantt = schedule_rr(processes, quantum=3)

    assert get_timeline(gantt) == [
        ("P1", 0, 3),
        ("P2", 3, 6),
        ("P3", 6, 8),
        ("P1", 8, 11),
        ("P2", 11, 12),
        ("P1", 12, 13),
    ]

    assert [r.pid for r in results] == [
        "P3", "P2", "P1"
    ]


def test_rr_preemptive_metrics():
    processes = [
        Process("P1", 0, 7),
        Process("P2", 2, 4),
        Process("P3", 3, 2),
    ]

    results, gantt = schedule_rr(processes, 3)

    by_pid = {r.pid: r for r in results}

    assert by_pid["P1"].start_time == 0
    assert by_pid["P1"].completion_time == 13
    assert by_pid["P1"].waiting_time == 6

    assert by_pid["P2"].start_time == 3
    assert by_pid["P2"].completion_time == 12
    assert by_pid["P2"].waiting_time == 6

    assert by_pid["P3"].start_time == 6
    assert by_pid["P3"].completion_time == 8
    assert by_pid["P3"].waiting_time == 3

    summary = SchedulingSummary(
        tuple(results), tuple(gantt)
    )

    assert summary.average_waiting_time == pytest.approx(5)
    assert summary.average_turnaround_time == pytest.approx(28 / 3)
    assert summary.average_response_time == pytest.approx(4 / 3)
    assert summary.cpu_busy_time == 13
    assert summary.cpu_utilization == pytest.approx(100)


def test_rr_single_process_multiple_quantums():
    processes = [Process("P1", 0, 5)]

    results, gantt = schedule_rr(processes, 2)

    assert get_timeline(gantt) == [
        ("P1", 0, 2),
        ("P1", 2, 4),
        ("P1", 4, 5),
    ]

    assert len(results) == 1
    assert results[0].waiting_time == 0


def test_rr_quantum_one():
    processes = [
        Process("P1", 0, 3),
        Process("P2", 0, 2),
    ]

    _, gantt = schedule_rr(processes, 1)

    assert get_timeline(gantt) == [
        ("P1", 0, 1),
        ("P2", 1, 2),
        ("P1", 2, 3),
        ("P2", 3, 4),
        ("P1", 4, 5),
    ]


def test_rr_arrivals_at_quantum_boundary():
    processes = [
        Process("P1", 0, 4),
        Process("P2", 2, 1),
    ]

    _, gantt = schedule_rr(processes, 2)

    assert get_timeline(gantt) == [
        ("P1", 0, 2),
        ("P2", 2, 3),
        ("P1", 3, 5),
    ]


def test_rr_handles_multiple_idle_intervals():
    processes = [
        Process("P1", 3, 3),
        Process("P2", 10, 1),
    ]

    results, gantt = schedule_rr(processes, 2)

    assert get_timeline(gantt) == [
        ("IDLE", 0, 3),
        ("P1", 3, 5),
        ("P1", 5, 6),
        ("IDLE", 6, 10),
        ("P2", 10, 11),
    ]

    summary = SchedulingSummary(
        tuple(results), tuple(gantt)
    )

    assert summary.cpu_busy_time == 4
    assert summary.cpu_idle_time == 7
    assert summary.makespan == 11


def test_rr_large_quantum_matches_fcfs():
    processes = [
        Process("P3", 2, 1),
        Process("P1", 0, 5),
        Process("P2", 1, 3),
    ]

    fcfs_results, fcfs_gantt = schedule_fcfs(processes)
    rr_results, rr_gantt = schedule_rr(processes, 10)

    assert get_timeline(rr_gantt) == get_timeline(fcfs_gantt)

    assert [
        (r.pid, r.start_time, r.completion_time)
        for r in rr_results
    ] == [
        (r.pid, r.start_time, r.completion_time)
        for r in fcfs_results
    ]


def test_rr_preserves_equal_arrival_order():
    processes = [
        Process("P2", 0, 3),
        Process("P1", 0, 2),
    ]

    _, gantt = schedule_rr(processes, 1)

    assert get_timeline(gantt) == [
        ("P2", 0, 1),
        ("P1", 1, 2),
        ("P2", 2, 3),
        ("P1", 3, 4),
        ("P2", 4, 5),
    ]


def test_rr_rejects_invalid_inputs():
    with pytest.raises(ValueError):
        schedule_rr([], 2)

    with pytest.raises(TypeError):
        schedule_rr(None, 2)

    processes = [Process("P1", 0, 3)]

    for quantum in (0, -1, True, 1.5, "2", None):
        with pytest.raises((ValueError, TypeError)):
            schedule_rr(processes, quantum)

    with pytest.raises(ValueError):
        schedule_rr([
            Process("P1", 0, 3),
            Process("P1", 1, 2),
        ], 2)


def test_rr_preserves_input_and_reuses_report():
    processes = [
        Process("P1", 0, 3),
        Process("P2", 0, 2),
    ]

    original = list(processes)

    results, gantt = schedule_rr(processes, 1)

    summary = SchedulingSummary(
        tuple(results), tuple(gantt)
    )

    report = render_scheduling_report(summary, "RR")

    assert processes == original
    assert "CPU SCHEDULING | RR" in report
    assert "PROCESS RESULTS" in report
    assert "CPU GANTT" in report
    assert "SCHEDULING SUMMARY" in report
