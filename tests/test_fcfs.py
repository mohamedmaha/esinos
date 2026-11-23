import pytest

from esinos.scheduling.process import Process
from esinos.scheduling.fcfs import schedule_fcfs


def test_fcfs_standard_case():
    processes = [
        Process("P1", 0, 5),
        Process("P2", 1, 3),
        Process("P3", 2, 1),
    ]

    results, gantt = schedule_fcfs(processes)

    assert [r.pid for r in results] == ["P1", "P2", "P3"]
    assert [r.completion_time for r in results] == [5, 8, 9]
    assert [r.waiting_time for r in results] == [0, 4, 6]
    assert [r.turnaround_time for r in results] == [5, 7, 7]

    assert [(g.label, g.start, g.end) for g in gantt] == [
        ("P1", 0, 5),
        ("P2", 5, 8),
        ("P3", 8, 9),
    ]

    assert sum(r.waiting_time for r in results) / 3 == pytest.approx(10 / 3)
    assert sum(r.turnaround_time for r in results) / 3 == pytest.approx(19 / 3)


def test_fcfs_idle_cpu():
    processes = [
        Process("P1", 2, 3),
        Process("P2", 4, 2),
        Process("P3", 9, 1),
    ]

    results, gantt = schedule_fcfs(processes)

    assert [(g.label, g.start, g.end) for g in gantt] == [
        ("IDLE", 0, 2),
        ("P1", 2, 5),
        ("P2", 5, 7),
        ("IDLE", 7, 9),
        ("P3", 9, 10),
    ]

    assert [r.waiting_time for r in results] == [0, 1, 0]


def test_fcfs_same_arrival_time():
    processes = [
        Process("P2", 0, 2),
        Process("P1", 0, 4),
        Process("P3", 1, 1),
    ]

    results, gantt = schedule_fcfs(processes)

    assert [r.pid for r in results] == ["P2", "P1", "P3"]
    assert [g.label for g in gantt] == ["P2", "P1", "P3"]


def test_fcfs_unsorted_input():
    processes = [
        Process("P3", 2, 1),
        Process("P1", 0, 5),
        Process("P2", 1, 3),
    ]

    results, _ = schedule_fcfs(processes)

    assert [r.pid for r in results] == ["P1", "P2", "P3"]


def test_fcfs_single_process():
    results, gantt = schedule_fcfs([
        Process("P1", 4, 2),
    ])

    assert results[0].start_time == 4
    assert results[0].completion_time == 6
    assert results[0].waiting_time == 0

    assert [(g.label, g.start, g.end) for g in gantt] == [
        ("IDLE", 0, 4),
        ("P1", 4, 6),
    ]


def test_fcfs_empty_input():
    with pytest.raises(ValueError):
        schedule_fcfs([])


def test_fcfs_duplicate_pid():
    processes = [
        Process("P1", 0, 2),
        Process("P1", 1, 3),
    ]

    with pytest.raises(ValueError):
        schedule_fcfs(processes)


def test_fcfs_invalid_process_object():
    with pytest.raises(TypeError):
        schedule_fcfs(["P1"])


def test_fcfs_does_not_modify_input():
    processes = [
        Process("P2", 2, 3),
        Process("P1", 0, 5),
    ]

    original_order = list(processes)

    schedule_fcfs(processes)

    assert processes == original_order
