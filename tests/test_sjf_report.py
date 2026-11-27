import pytest

from esinos.scheduling.process import Process
from esinos.scheduling.fcfs import schedule_fcfs
from esinos.scheduling.sjf import schedule_sjf
from esinos.scheduling.summary import SchedulingSummary

from esinos.ui.report import render_scheduling_report
from esinos.ui.gantt import render_gantt
from esinos.ui.table import render_process_table


def make_summary(processes, scheduler):
    results, gantt = scheduler(processes)

    return SchedulingSummary(
        results=tuple(results),
        gantt=tuple(gantt),
    )


def test_sjf_report_contains_all_sections():
    processes = [
        Process("P1", 0, 7),
        Process("P2", 2, 4),
        Process("P3", 4, 1),
        Process("P4", 5, 4),
    ]

    summary = make_summary(processes, schedule_sjf)

    output = render_scheduling_report(summary, "SJF")

    assert "CPU SCHEDULING | SJF" in output
    assert "PROCESS RESULTS" in output
    assert "CPU GANTT" in output
    assert "SCHEDULING SUMMARY" in output

    assert "Average Waiting Time: 4.00" in output
    assert "Average Turnaround Time: 8.00" in output
    assert "CPU Utilization: 100.00%" in output


def test_sjf_report_reuses_existing_renderers():
    processes = [
        Process("P1", 0, 7),
        Process("P2", 2, 4),
        Process("P3", 4, 1),
    ]

    summary = make_summary(processes, schedule_sjf)

    output = render_scheduling_report(summary, "SJF")

    assert render_process_table(summary) in output
    assert render_gantt(summary) in output


def test_sjf_report_with_idle_intervals():
    processes = [
        Process("P1", 2, 4),
        Process("P2", 3, 1),
        Process("P3", 8, 2),
    ]

    summary = make_summary(processes, schedule_sjf)

    output = render_scheduling_report(summary, "SJF")

    assert "IDLE" in output
    assert "CPU Busy Time: 7" in output
    assert "CPU Idle Time: 3" in output
    assert "Makespan: 10" in output
    assert "CPU Utilization: 70.00%" in output


def test_sjf_vs_fcfs_comparison():
    processes = [
        Process("P1", 0, 7),
        Process("P2", 2, 4),
        Process("P3", 4, 1),
        Process("P4", 5, 4),
    ]

    fcfs = make_summary(processes, schedule_fcfs)
    sjf = make_summary(processes, schedule_sjf)

    assert fcfs.average_waiting_time == pytest.approx(4.75)
    assert sjf.average_waiting_time == pytest.approx(4.0)

    assert fcfs.average_turnaround_time == pytest.approx(8.75)
    assert sjf.average_turnaround_time == pytest.approx(8.0)

    assert sjf.average_waiting_time < fcfs.average_waiting_time


def test_sjf_report_preserves_data():
    processes = [
        Process("P1", 0, 5),
        Process("P2", 1, 2),
    ]

    original = list(processes)

    summary = make_summary(processes, schedule_sjf)

    original_results = summary.results
    original_gantt = summary.gantt

    render_scheduling_report(summary, "SJF")

    assert processes == original
    assert summary.results == original_results
    assert summary.gantt == original_gantt
