import pytest

from esinos.scheduling.process import Process
from esinos.scheduling.fcfs import schedule_fcfs
from esinos.scheduling.sjf import schedule_sjf
from esinos.scheduling.summary import SchedulingSummary
from esinos.ui.comparison import render_scheduling_comparison


def make_summary(processes, scheduler):
    results, gantt = scheduler(processes)

    return SchedulingSummary(
        results=tuple(results),
        gantt=tuple(gantt),
    )


def test_comparison_standard_scenario():
    processes = [
        Process("P1", 0, 5),
        Process("P2", 1, 3),
        Process("P3", 2, 1),
    ]

    fcfs = make_summary(processes, schedule_fcfs)
    sjf = make_summary(processes, schedule_sjf)

    output = render_scheduling_comparison(fcfs, sjf)

    assert "FCFS VS SJF COMPARISON" in output
    assert "Average WT" in output
    assert "Average TAT" in output
    assert "CPU Utilization" in output

    assert "FCFS: P1 -> P2 -> P3" in output
    assert "SJF : P1 -> P3 -> P2" in output

    assert "Average WT improvement with SJF: 20.00%" in output
    assert "Best average WT: SJF" in output


def test_comparison_with_idle_cpu():
    processes = [
        Process("P1", 2, 4),
        Process("P2", 3, 1),
        Process("P3", 8, 2),
    ]

    fcfs = make_summary(processes, schedule_fcfs)
    sjf = make_summary(processes, schedule_sjf)

    output = render_scheduling_comparison(fcfs, sjf)

    assert "CPU Idle Time" in output
    assert "CPU Utilization" in output
    assert "70.00%" in output


def test_comparison_with_zero_waiting_time():
    processes = [
        Process("P1", 0, 3),
    ]

    fcfs = make_summary(processes, schedule_fcfs)
    sjf = make_summary(processes, schedule_sjf)

    output = render_scheduling_comparison(fcfs, sjf)

    assert "Average WT improvement with SJF: N/A" in output
    assert "Best average WT: Tie" in output


def test_comparison_rejects_invalid_types():
    processes = [Process("P1", 0, 3)]

    fcfs = make_summary(processes, schedule_fcfs)

    with pytest.raises(TypeError):
        render_scheduling_comparison("invalid", fcfs)

    with pytest.raises(TypeError):
        render_scheduling_comparison(fcfs, None)


def test_comparison_rejects_different_workloads():
    fcfs_processes = [
        Process("P1", 0, 5),
    ]

    sjf_processes = [
        Process("P1", 0, 2),
    ]

    fcfs = make_summary(fcfs_processes, schedule_fcfs)
    sjf = make_summary(sjf_processes, schedule_sjf)

    with pytest.raises(ValueError):
        render_scheduling_comparison(fcfs, sjf)


def test_comparison_preserves_summaries():
    processes = [
        Process("P1", 0, 5),
        Process("P2", 1, 2),
    ]

    fcfs = make_summary(processes, schedule_fcfs)
    sjf = make_summary(processes, schedule_sjf)

    original_fcfs = (fcfs.results, fcfs.gantt)
    original_sjf = (sjf.results, sjf.gantt)

    render_scheduling_comparison(fcfs, sjf)

    assert (fcfs.results, fcfs.gantt) == original_fcfs
    assert (sjf.results, sjf.gantt) == original_sjf
