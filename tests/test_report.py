import pytest

from esinos.scheduling.process import Process
from esinos.scheduling.fcfs import schedule_fcfs
from esinos.scheduling.summary import SchedulingSummary
from esinos.ui.report import render_scheduling_report


def make_summary(processes):
    results, gantt = schedule_fcfs(processes)
    return SchedulingSummary(tuple(results), tuple(gantt))


def test_report_standard_case():
    summary = make_summary([
        Process("P1", 0, 5),
        Process("P2", 1, 3),
        Process("P3", 2, 1),
    ])

    output = render_scheduling_report(summary, "FCFS")

    assert "ESINOS | CPU SCHEDULING | FCFS" in output
    assert "PROCESS RESULTS" in output
    assert "CPU GANTT" in output
    assert "SCHEDULING SUMMARY" in output

    assert "Average Waiting Time: 3.33" in output
    assert "Average Turnaround Time: 6.33" in output
    assert "CPU Utilization: 100.00%" in output


def test_report_with_idle_cpu():
    summary = make_summary([
        Process("P1", 2, 3),
        Process("P2", 9, 1),
    ])

    output = render_scheduling_report(summary, "FCFS")

    assert "IDLE" in output
    assert "CPU Busy Time: 4" in output
    assert "CPU Idle Time: 6" in output
    assert "CPU Utilization: 40.00%" in output


def test_report_supports_other_algorithm_names():
    summary = make_summary([
        Process("P1", 0, 3),
    ])

    output = render_scheduling_report(summary, "SJF")

    assert "CPU SCHEDULING | SJF" in output


def test_report_rejects_invalid_arguments():
    summary = make_summary([
        Process("P1", 0, 3),
    ])

    with pytest.raises(TypeError):
        render_scheduling_report("invalid", "FCFS")

    with pytest.raises(ValueError):
        render_scheduling_report(summary, "   ")


def test_report_does_not_modify_summary():
    summary = make_summary([
        Process("P1", 0, 3),
    ])

    original_results = summary.results
    original_gantt = summary.gantt

    render_scheduling_report(summary, "FCFS")

    assert summary.results == original_results
    assert summary.gantt == original_gantt
