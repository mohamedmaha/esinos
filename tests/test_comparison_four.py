import pytest

from esinos.scheduling.process import Process
from esinos.scheduling.fcfs import schedule_fcfs
from esinos.scheduling.sjf import schedule_sjf
from esinos.scheduling.rr import schedule_rr
from esinos.scheduling.priority import schedule_priority
from esinos.scheduling.summary import SchedulingSummary
from esinos.ui.comparison_four import (
    render_four_way_comparison,
)


def make_summary(scheduler, processes, **kwargs):
    results, gantt = scheduler(processes, **kwargs)

    return SchedulingSummary(
        tuple(results),
        tuple(gantt),
    )


def make_four(processes, quantum=2):
    return (
        make_summary(schedule_fcfs, processes),
        make_summary(schedule_sjf, processes),
        make_summary(
            schedule_rr, processes, quantum=quantum
        ),
        make_summary(schedule_priority, processes),
    )


def reference_processes():
    return [
        Process("P1", 0, 5, priority=3),
        Process("P2", 1, 3, priority=1),
        Process("P3", 2, 1, priority=2),
    ]


def test_four_way_reference_scenario():
    summaries = make_four(reference_processes())

    output = render_four_way_comparison(
        *summaries, quantum=2
    )

    assert (
        "ESINOS - FOUR-WAY SCHEDULING COMPARISON"
        in output
    )

    assert "RR(q=2)" in output
    assert "PRIORITY" in output
    assert "Best average WT: SJF" in output
    assert "Best average RT: RR" in output

    average_wt_row = next(
        line for line in output.splitlines()
        if line.startswith("Average WT")
    )

    values = [
        value.strip()
        for value in average_wt_row.split("|")[1:]
    ]

    assert values == [
        "3.33", "2.67", "3.33", "3.33"
    ]


def test_priority_execution_order_is_reported():
    processes = [
        Process("P1", 0, 6, priority=3),
        Process("P2", 1, 2, priority=1),
        Process("P3", 2, 4, priority=2),
        Process("P4", 4, 1, priority=1),
    ]

    summaries = make_four(processes)

    output = render_four_way_comparison(
        *summaries, quantum=2
    )

    assert (
        "PRIORITY: P1 -> P2 -> P4 -> P3"
        in output
    )

    assert "FCFS: P1 -> P2 -> P3 -> P4" in output


def test_four_way_single_process_tie():
    processes = [
        Process("P1", 0, 3, priority=2)
    ]

    summaries = make_four(processes)

    output = render_four_way_comparison(
        *summaries, quantum=2
    )

    expected = "FCFS / SJF / RR / PRIORITY"

    assert f"Best average WT: {expected}" in output
    assert f"Best average RT: {expected}" in output


def test_four_way_handles_idle_intervals():
    processes = [
        Process("P1", 2, 4, priority=2),
        Process("P2", 3, 1, priority=1),
        Process("P3", 8, 2, priority=3),
    ]

    summaries = make_four(processes)

    output = render_four_way_comparison(
        *summaries, quantum=2
    )

    assert "CPU Idle Time" in output
    assert "70.00%" in output
    assert "IDLE[0-2]" in output


def test_four_way_rejects_different_workloads():
    processes = reference_processes()

    changed = [
        Process("P1", 0, 5, priority=3),
        Process("P2", 1, 3, priority=9),
        Process("P3", 2, 1, priority=2),
    ]

    fcfs, sjf, rr, _ = make_four(processes)

    different_priority = make_summary(
        schedule_priority, changed
    )

    with pytest.raises(ValueError):
        render_four_way_comparison(
            fcfs, sjf, rr, different_priority, 2
        )


def test_four_way_rejects_invalid_summaries():
    fcfs, sjf, rr, priority = make_four(
        reference_processes()
    )

    with pytest.raises(TypeError):
        render_four_way_comparison(
            None, sjf, rr, priority, 2
        )

    with pytest.raises(TypeError):
        render_four_way_comparison(
            fcfs, sjf, "invalid", priority, 2
        )

    with pytest.raises(TypeError):
        render_four_way_comparison(
            fcfs, sjf, rr, None, 2
        )


def test_four_way_rejects_invalid_quantum():
    summaries = make_four(reference_processes())

    for quantum in (None, True, 2.5, "2"):
        with pytest.raises(TypeError):
            render_four_way_comparison(
                *summaries, quantum=quantum
            )

    for quantum in (0, -3):
        with pytest.raises(ValueError):
            render_four_way_comparison(
                *summaries, quantum=quantum
            )


def test_four_way_preserves_summaries():
    processes = reference_processes()
    original_processes = list(processes)

    summaries = make_four(processes)

    originals = [
        (summary.results, summary.gantt)
        for summary in summaries
    ]

    render_four_way_comparison(
        *summaries, quantum=2
    )

    for summary, original in zip(
        summaries, originals
    ):
        assert (
            summary.results, summary.gantt
        ) == original

    assert processes == original_processes
