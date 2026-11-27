import pytest

from esinos.scheduling.process import Process
from esinos.scheduling.sjf import (
    _validate_processes,
    _select_shortest_ready,
)


def test_sjf_valid_input():
    processes = [
        Process("P1", 0, 5),
        Process("P2", 1, 3),
    ]

    assert _validate_processes(processes) is None


def test_sjf_rejects_empty_input():
    with pytest.raises(ValueError):
        _validate_processes([])


def test_sjf_rejects_invalid_collection():
    with pytest.raises(TypeError):
        _validate_processes(None)


def test_sjf_rejects_invalid_process():
    with pytest.raises(TypeError):
        _validate_processes([
            Process("P1", 0, 3),
            "invalid",
        ])


def test_sjf_rejects_duplicate_pid():
    processes = [
        Process("P1", 0, 4),
        Process("P1", 1, 2),
    ]

    with pytest.raises(ValueError):
        _validate_processes(processes)


def test_sjf_selects_shortest_ready():
    pending = [
        Process("P1", 0, 5),
        Process("P2", 1, 2),
        Process("P3", 2, 1),
    ]

    selected = _select_shortest_ready(pending, 4)

    assert selected.pid == "P3"


def test_sjf_ignores_future_arrivals():
    pending = [
        Process("P1", 0, 5),
        Process("P2", 8, 1),
    ]

    selected = _select_shortest_ready(pending, 0)

    assert selected.pid == "P1"


def test_sjf_returns_none_when_cpu_idle():
    pending = [
        Process("P1", 5, 2),
        Process("P2", 8, 1),
    ]

    selected = _select_shortest_ready(pending, 0)

    assert selected is None


def test_sjf_breaks_ties_by_arrival():
    pending = [
        Process("P1", 4, 2),
        Process("P2", 1, 2),
    ]

    selected = _select_shortest_ready(pending, 5)

    assert selected.pid == "P2"


def test_sjf_preserves_order_on_full_tie():
    pending = [
        Process("P1", 0, 3),
        Process("P2", 0, 3),
    ]

    selected = _select_shortest_ready(pending, 0)

    assert selected.pid == "P1"


def test_sjf_selection_does_not_modify_input():
    pending = [
        Process("P1", 0, 8),
        Process("P2", 0, 2),
    ]

    original = list(pending)

    _select_shortest_ready(pending, 0)

    assert pending == original
