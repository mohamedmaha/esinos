import pytest

from esinos.scheduling.process import Process
from esinos.scheduling.fcfs import schedule_fcfs
from esinos.scheduling.sjf import schedule_sjf
from esinos.scheduling.rr import schedule_rr
from esinos.scheduling.summary import SchedulingSummary
from esinos.ui.comparison_three import (
    render_three_way_comparison,
)


def make_summary(scheduler, processes, **kwargs):
    results, gantt = scheduler(processes, **kwargs)

    return SchedulingSummary(
        results=tuple(results),
        gantt=tuple(gantt),
    )


def make_three(processes, quantum=2):
    return (
        make_summary(schedule_fcfs, processes),
        make_summary(schedule_sjf, processes),
        make_summary(
            schedule_rr, processes, quantum=quantum
        ),
    )


def test_three_way_standard_comparison():
    processes = [
        Process("P1", 0, 5),
        Process("P2", 1, 3),
        Process("P3", 2, 1),
    ]

    fcfs, sjf, rr = make_three(processes)

    output = render_three_way_comparison(
        fcfs, sjf, rr, 2
    )

    assert "FCFS VS SJF VS ROUND ROBIN" in output
    assert "RR(q=2)" in output

    assert "Best average WT: SJF" in output
    assert "Best average RT: RR" in output

    assert "FCFS: P1 -> P2 -> P3" in output
    assert "SJF : P1 -> P3 -> P2" in output

    assert "P1[0-2]" in output
    assert "P3[4-5]" in output

    average_wt_row = next(
        line for line in output.splitlines()
        if line.startswith("Average WT")
    )

    values = [
        value.strip()
        for value in average_wt_row.split("|")[1:]
    ]

    assert values == ["3.33", "2.67", "3.33"]


def test_three_way_idle_intervals():
    processes = [
        Process("P1", 2, 4),
        Process("P2", 3, 1),
        Process("P3", 8, 2),
    ]

    fcfs, sjf, rr = make_three(processes)

    output = render_three_way_comparison(
        fcfs, sjf, rr, 2
    )

    assert "CPU Idle Time" in output
    assert "70.00%" in output
    assert "IDLE[0-2]" in output


def test_three_way_all_algorithms_tie():
    processes = [
        Process("P1", 0, 3),
    ]

    fcfs, sjf, rr = make_three(processes)

    output = render_three_way_comparison(
        fcfs, sjf, rr, 2
    )

    assert (
        "Best average WT: FCFS / SJF / RR"
        in output
    )

    assert (
        "Best average RT: FCFS / SJF / RR"
        in output
    )


def test_three_way_rejects_invalid_types():
    processes = [Process("P1", 0, 3)]

    fcfs, sjf, rr = make_three(processes)

    with pytest.raises(TypeError):
        render_three_way_comparison(
            None, sjf, rr, 2
        )

    with pytest.raises(TypeError):
        render_three_way_comparison(
            fcfs, "invalid", rr, 2
        )

    with pytest.raises(TypeError):
        render_three_way_comparison(
            fcfs, sjf, None, 2
        )


def test_three_way_rejects_different_workloads():
    processes = [Process("P1", 0, 5)]
    changed = [Process("P1", 0, 4)]

    fcfs = make_summary(schedule_fcfs, processes)
    sjf = make_summary(schedule_sjf, processes)
    rr = make_summary(
        schedule_rr, changed, quantum=2
    )

    with pytest.raises(ValueError):
        render_three_way_comparison(
            fcfs, sjf, rr, 2
        )


def test_three_way_rejects_invalid_quantum():
    processes = [Process("P1", 0, 3)]
    fcfs, sjf, rr = make_three(processes)

    for value in (None, True, 2.5, "2"):
        with pytest.raises(TypeError):
            render_three_way_comparison(
                fcfs, sjf, rr, value
            )

    for value in (0, -1):
        with pytest.raises(ValueError):
            render_three_way_comparison(
                fcfs, sjf, rr, value
            )


def test_three_way_preserves_summaries():
    processes = [
        Process("P1", 0, 5),
        Process("P2", 1, 3),
        Process("P3", 2, 1),
    ]

    fcfs, sjf, rr = make_three(processes)

    originals = [
        (summary.results, summary.gantt)
        for summary in (fcfs, sjf, rr)
    ]

    render_three_way_comparison(fcfs, sjf, rr, 2)

    for summary, original in zip(
        (fcfs, sjf, rr), originals
    ):
        assert (
            summary.results, summary.gantt
        ) == original
