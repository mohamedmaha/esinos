import pytest

from esinos.scheduling.process import Process
from esinos.scheduling.fcfs import schedule_fcfs
from esinos.scheduling.summary import SchedulingSummary
from esinos.ui.gantt import render_gantt


def make_summary(processes):
    results, gantt = schedule_fcfs(processes)
    return SchedulingSummary(tuple(results), tuple(gantt))


def test_gantt_standard_case():
    summary = make_summary([
        Process("P1", 0, 5),
        Process("P2", 1, 3),
        Process("P3", 2, 1),
    ])

    output = render_gantt(summary)
    lines = output.splitlines()

    assert lines[0] == "CPU GANTT"
    assert "P1" in lines[1]
    assert "P2" in lines[1]
    assert "P3" in lines[1]
    assert lines[2].split() == ["0", "5", "8", "9"]


def test_gantt_idle_intervals():
    summary = make_summary([
        Process("P1", 2, 3),
        Process("P2", 9, 1),
    ])

    output = render_gantt(summary)

    assert output.count("IDLE") == 2
    assert "P1" in output
    assert "P2" in output


def test_gantt_proportional_width():
    summary = make_summary([
        Process("P1", 0, 5),
        Process("P2", 1, 3),
        Process("P3", 2, 1),
    ])

    bar = render_gantt(summary).splitlines()[1]
    blocks = bar.split("|")[1:-1]

    assert len(blocks[0]) > len(blocks[1])
    assert len(blocks[1]) > len(blocks[2])


def test_gantt_invalid_width():
    summary = make_summary([Process("P1", 0, 3)])

    with pytest.raises(ValueError):
        render_gantt(summary, unit_width=0)


def test_gantt_does_not_modify_summary():
    summary = make_summary([Process("P1", 0, 3)])
    original_gantt = summary.gantt

    render_gantt(summary)

    assert summary.gantt == original_gantt
