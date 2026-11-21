import pytest

from esinos.scheduling.result import GanttSegment, ProcessResult
from dataclasses import FrozenInstanceError
from esinos.scheduling.process import Process


def test_valid_segment():
    segment = GanttSegment("P1", 0, 5)

    assert segment.pid == "P1"
    assert segment.start == 0
    assert segment.end == 5
    assert segment.duration == 5
    assert segment.label == "P1"


def test_idle_segment():
    segment = GanttSegment(None, 5, 8)

    assert segment.duration == 3
    assert segment.label == "IDLE"


@pytest.mark.parametrize(
    "start,end",
    [
        (0, 0),
        (5, 3),
        (-1, 3),
        (True, 3),
        (0, 2.5),
    ],
)
def test_invalid_segment_times(start, end):
    with pytest.raises(ValueError):
        GanttSegment("P1", start, end)


@pytest.mark.parametrize("pid", ["", "   ", 123])
def test_invalid_segment_pid(pid):
    with pytest.raises(ValueError):
        GanttSegment(pid, 0, 5)


def test_process_result_fcfs_metrics():
    process = Process("P2", 1, 3)
    result = ProcessResult(process, 5, 8)

    assert result.pid == "P2"
    assert result.start_time == 5
    assert result.completion_time == 8
    assert result.turnaround_time == 7
    assert result.waiting_time == 4
    assert result.response_time == 4


def test_process_result_preemptive_metrics():
    process = Process("P1", 0, 5)
    result = ProcessResult(process, 0, 9)

    assert result.turnaround_time == 9
    assert result.waiting_time == 4
    assert result.response_time == 0


def test_invalid_process_result_object():
    with pytest.raises(TypeError):
        ProcessResult("P1", 0, 5)


@pytest.mark.parametrize(
    "start,completion",
    [
        (0, 7),
        (1, 4),
        (True, 7),
        (1, 7.5),
    ],
)
def test_invalid_process_result_times(start, completion):
    process = Process("P1", 1, 4)

    with pytest.raises(ValueError):
        ProcessResult(process, start, completion)


def test_process_result_is_immutable():
    process = Process("P1", 0, 5)
    result = ProcessResult(process, 0, 5)

    with pytest.raises(FrozenInstanceError):
        result.completion_time = 10
