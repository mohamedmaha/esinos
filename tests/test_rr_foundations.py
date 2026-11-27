from collections import deque

import pytest

from esinos.scheduling.process import Process
from esinos.scheduling.rr import (
    _validate_rr_inputs,
    _enqueue_arrivals,
)


def test_rr_accepts_valid_inputs():
    processes = (
        Process("P1", 0, 5),
        Process("P2", 2, 3),
    )

    assert _validate_rr_inputs(processes, 2) is None


def test_rr_rejects_empty_input():
    with pytest.raises(ValueError):
        _validate_rr_inputs([], 2)


def test_rr_rejects_invalid_collection():
    for invalid in (None, "P1", 123):
        with pytest.raises(TypeError):
            _validate_rr_inputs(invalid, 2)


def test_rr_rejects_invalid_process():
    processes = [
        Process("P1", 0, 5),
        "invalid",
    ]

    with pytest.raises(TypeError):
        _validate_rr_inputs(processes, 2)


def test_rr_rejects_duplicate_pids():
    processes = [
        Process("P1", 0, 5),
        Process("P1", 2, 3),
    ]

    with pytest.raises(ValueError):
        _validate_rr_inputs(processes, 2)


def test_rr_rejects_invalid_quantum():
    processes = [Process("P1", 0, 5)]

    for quantum in (0, -2, True, 2.5, "2", None):
        with pytest.raises((TypeError, ValueError)):
            _validate_rr_inputs(processes, quantum)


def test_rr_enqueues_initial_arrivals():
    ordered = [
        Process("P1", 0, 5),
        Process("P2", 0, 2),
        Process("P3", 2, 1),
    ]

    ready = deque()

    index = _enqueue_arrivals(
        ordered, 0, 0, ready
    )

    assert index == 2
    assert [p.pid for p in ready] == ["P1", "P2"]


def test_rr_arrivals_precede_requeued_process():
    ordered = [
        Process("P1", 0, 7),
        Process("P2", 2, 4),
        Process("P3", 3, 2),
    ]

    ready = deque()

    index = _enqueue_arrivals(
        ordered, 0, 0, ready
    )

    running = ready.popleft()

    # P1 executes from time 0 to time 3.
    index = _enqueue_arrivals(
        ordered, index, 3, ready
    )

    # P1 did not finish, so it returns last.
    ready.append(running)

    assert index == 3
    assert [p.pid for p in ready] == [
        "P2", "P3", "P1"
    ]


def test_rr_does_not_enqueue_future_or_duplicate():
    ordered = [
        Process("P1", 4, 2),
        Process("P2", 7, 3),
    ]

    ready = deque()

    index = _enqueue_arrivals(
        ordered, 0, 3, ready
    )

    assert index == 0
    assert list(ready) == []

    index = _enqueue_arrivals(
        ordered, index, 4, ready
    )

    assert index == 1
    assert [p.pid for p in ready] == ["P1"]

    index = _enqueue_arrivals(
        ordered, index, 4, ready
    )

    assert index == 1
    assert [p.pid for p in ready] == ["P1"]


def test_rr_preserves_order_of_equal_arrivals():
    processes = [
        Process("P3", 3, 1),
        Process("P2", 0, 4),
        Process("P1", 0, 3),
    ]

    original = list(processes)

    ordered = sorted(
        processes,
        key=lambda p: p.arrival_time,
    )

    ready = deque()

    index = _enqueue_arrivals(
        ordered, 0, 0, ready
    )

    assert index == 2
    assert [p.pid for p in ready] == ["P2", "P1"]
    assert processes == original
