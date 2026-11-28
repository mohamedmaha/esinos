import pytest

from esinos.scheduling.process import Process
from esinos.scheduling.priority import (
    _validate_priority_inputs,
    _select_highest_priority_ready,
)


def test_priority_accepts_valid_inputs():
    processes = [
        Process("P1", 0, 5, priority=3),
        Process("P2", 2, 3, priority=1),
    ]

    assert _validate_priority_inputs(processes) is None


def test_priority_rejects_empty_input():
    with pytest.raises(ValueError):
        _validate_priority_inputs([])


def test_priority_rejects_invalid_collection():
    for invalid in (None, "P1", 123):
        with pytest.raises(TypeError):
            _validate_priority_inputs(invalid)


def test_priority_rejects_invalid_process():
    processes = [
        Process("P1", 0, 5, priority=1),
        "invalid",
    ]

    with pytest.raises(TypeError):
        _validate_priority_inputs(processes)


def test_priority_rejects_duplicate_pids():
    processes = [
        Process("P1", 0, 5, priority=2),
        Process("P1", 1, 3, priority=1),
    ]

    with pytest.raises(ValueError):
        _validate_priority_inputs(processes)


def test_priority_selects_highest_priority():
    processes = [
        Process("P1", 0, 5, priority=3),
        Process("P2", 0, 2, priority=1),
        Process("P3", 0, 1, priority=2),
    ]

    selected = _select_highest_priority_ready(
        processes, current_time=0
    )

    assert selected.pid == "P2"


def test_priority_ignores_future_arrivals():
    processes = [
        Process("P1", 0, 5, priority=3),
        Process("P2", 5, 2, priority=1),
    ]

    selected = _select_highest_priority_ready(
        processes, current_time=0
    )

    assert selected.pid == "P1"


def test_priority_tie_uses_earlier_arrival():
    processes = [
        Process("P2", 4, 2, priority=1),
        Process("P1", 1, 5, priority=1),
    ]

    selected = _select_highest_priority_ready(
        processes, current_time=5
    )

    assert selected.pid == "P1"


def test_priority_tie_preserves_input_order():
    processes = [
        Process("P3", 0, 1, priority=2),
        Process("P1", 0, 5, priority=1),
        Process("P2", 0, 2, priority=1),
    ]

    selected = _select_highest_priority_ready(
        processes, current_time=0
    )

    assert selected.pid == "P1"


def test_priority_returns_none_if_not_ready():
    processes = [
        Process("P1", 5, 3, priority=1),
        Process("P2", 8, 2, priority=2),
    ]

    selected = _select_highest_priority_ready(
        processes, current_time=3
    )

    assert selected is None


def test_priority_selection_preserves_inputs():
    processes = [
        Process("P1", 0, 4, priority=2),
        Process("P2", 0, 1, priority=1),
    ]

    original = list(processes)

    _select_highest_priority_ready(
        processes, current_time=0
    )

    assert processes == original
