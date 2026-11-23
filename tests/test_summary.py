import pytest

from esinos.scheduling.process import Process
from esinos.scheduling.result import GanttSegment, ProcessResult
from esinos.scheduling.fcfs import schedule_fcfs
from esinos.scheduling.summary import SchedulingSummary


def make_summary(processes):
    results, gantt = schedule_fcfs(processes)
    return SchedulingSummary(tuple(results), tuple(gantt))


def test_standard_summary():
    summary = make_summary([
        Process("P1", 0, 5),
        Process("P2", 1, 3),
        Process("P3", 2, 1),
    ])

    assert summary.process_count == 3
    assert summary.average_waiting_time == pytest.approx(10 / 3)
    assert summary.average_turnaround_time == pytest.approx(19 / 3)
    assert summary.average_response_time == pytest.approx(10 / 3)
    assert summary.cpu_busy_time == 9
    assert summary.cpu_idle_time == 0
    assert summary.makespan == 9
    assert summary.cpu_utilization == pytest.approx(100)


def test_summary_with_idle_cpu():
    summary = make_summary([
        Process("P1", 2, 3),
        Process("P2", 4, 2),
        Process("P3", 9, 1),
    ])

    assert summary.cpu_busy_time == 6
    assert summary.cpu_idle_time == 4
    assert summary.makespan == 10
    assert summary.cpu_utilization == pytest.approx(60)
    assert summary.average_waiting_time == pytest.approx(1 / 3)
    assert summary.average_turnaround_time == pytest.approx(7 / 3)


def test_summary_supports_preemptive_segments():
    p1 = Process("P1", 0, 5)
    p2 = Process("P2", 1, 4)

    results = (
        ProcessResult(p1, 0, 9),
        ProcessResult(p2, 2, 6),
    )

    gantt = (
        GanttSegment("P1", 0, 2),
        GanttSegment("P2", 2, 6),
        GanttSegment("P1", 6, 9),
    )

    summary = SchedulingSummary(results, gantt)

    assert summary.cpu_busy_time == 9
    assert summary.average_waiting_time == pytest.approx(2.5)
    assert summary.average_response_time == pytest.approx(0.5)


def test_summary_rejects_empty_data():
    with pytest.raises(ValueError):
        SchedulingSummary((), ())


def test_summary_requires_tuples():
    with pytest.raises(TypeError):
        SchedulingSummary([], [])


def test_summary_rejects_gantt_gap():
    p1 = Process("P1", 0, 2)

    with pytest.raises(ValueError):
        SchedulingSummary(
            (ProcessResult(p1, 0, 2),),
            (
                GanttSegment("P1", 0, 1),
                GanttSegment("P1", 2, 3),
            ),
        )


def test_summary_rejects_unknown_pid():
    p1 = Process("P1", 0, 2)

    with pytest.raises(ValueError):
        SchedulingSummary(
            (ProcessResult(p1, 0, 2),),
            (GanttSegment("P2", 0, 2),),
        )


def test_summary_rejects_cpu_duration_mismatch():
    p1 = Process("P1", 0, 3)

    with pytest.raises(ValueError):
        SchedulingSummary(
            (ProcessResult(p1, 0, 3),),
            (GanttSegment("P1", 0, 2),),
        )


def test_summary_rejects_completion_mismatch():
    p1 = Process("P1", 0, 2)

    with pytest.raises(ValueError):
        SchedulingSummary(
            (ProcessResult(p1, 0, 3),),
            (
                GanttSegment("P1", 0, 2),
                GanttSegment(None, 2, 3),
            ),
        )


def test_summary_rejects_duplicate_results():
    p1 = Process("P1", 0, 2)
    result = ProcessResult(p1, 0, 2)

    with pytest.raises(ValueError):
        SchedulingSummary(
            (result, result),
            (GanttSegment("P1", 0, 2),),
        )
