from dataclasses import FrozenInstanceError

import pytest

from esinos.scheduling.process import Process


def test_valid_process():
    process = Process("P1", 0, 5, 2)

    assert process.pid == "P1"
    assert process.arrival_time == 0
    assert process.burst_time == 5
    assert process.priority == 2


def test_default_priority():
    process = Process("P2", 1, 4)

    assert process.priority == 1


@pytest.mark.parametrize("pid", ["", "   ", None, 123])
def test_invalid_pid(pid):
    with pytest.raises(ValueError):
        Process(pid, 0, 5)


@pytest.mark.parametrize("arrival", [-1, 1.5, True])
def test_invalid_arrival_time(arrival):
    with pytest.raises(ValueError):
        Process("P1", arrival, 5)


@pytest.mark.parametrize("burst", [0, -3, 2.5, True])
def test_invalid_burst_time(burst):
    with pytest.raises(ValueError):
        Process("P1", 0, burst)


@pytest.mark.parametrize("priority", [0, -1, 2.5, True])
def test_invalid_priority(priority):
    with pytest.raises(ValueError):
        Process("P1", 0, 5, priority)


def test_process_is_immutable():
    process = Process("P1", 0, 5)

    with pytest.raises(FrozenInstanceError):
        process.burst_time = 10
