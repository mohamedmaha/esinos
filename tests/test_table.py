import pytest

from esinos.scheduling.process import Process
from esinos.scheduling.fcfs import schedule_fcfs
from esinos.scheduling.summary import SchedulingSummary
from esinos.ui.table import render_process_table


def make_summary(processes):
    results, gantt = schedule_fcfs(processes)
    return SchedulingSummary(tuple(results), tuple(gantt))


def extract_table_rows(output):
    lines = [
        line for line in output.splitlines()
        if line.startswith("|")
    ]

    return [
        [cell.strip() for cell in line.strip("|").split("|")]
        for line in lines
    ]


def test_table_displays_correct_metrics():
    summary = make_summary([
        Process("P1", 0, 5),
        Process("P2", 1, 3),
        Process("P3", 2, 1),
    ])

    output = render_process_table(summary)
    rows = extract_table_rows(output)

    assert rows == [
        ["PID", "AT", "BT", "ST", "CT", "WT", "TAT", "RT"],
        ["P1", "0", "5", "0", "5", "0", "5", "0"],
        ["P2", "1", "3", "5", "8", "4", "7", "4"],
        ["P3", "2", "1", "8", "9", "6", "7", "6"],
    ]


def test_table_excludes_idle_segments():
    summary = make_summary([
        Process("P1", 2, 3),
        Process("P2", 9, 1),
    ])

    output = render_process_table(summary)
    rows = extract_table_rows(output)

    assert len(rows) == 3
    assert "IDLE" not in output


def test_table_handles_large_values():
    summary = make_summary([
        Process("LONG_PROCESS_IDENTIFIER", 120, 2),
    ])

    rows = extract_table_rows(render_process_table(summary))

    assert rows[1] == [
        "LONG_PROCESS_IDENTIFIER",
        "120", "2", "120",
        "122", "0", "2", "0",
    ]


def test_table_rejects_invalid_input():
    with pytest.raises(TypeError):
        render_process_table("not a summary")


def test_table_preserves_summary():
    summary = make_summary([
        Process("P1", 0, 3),
    ])

    original_results = summary.results
    original_gantt = summary.gantt

    render_process_table(summary)

    assert summary.results == original_results
    assert summary.gantt == original_gantt
