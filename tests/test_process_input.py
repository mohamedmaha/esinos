import pytest

from esinos.scheduling.process import Process
from esinos.scheduling.fcfs import schedule_fcfs
from esinos.scheduling.sjf import schedule_sjf
from esinos.scheduling.rr import schedule_rr
from esinos.scheduling.priority import schedule_priority

from esinos.ui.process_input import read_processes


def scripted_reader(*answers):
    """Create a fake interactive input function."""
    iterator = iter(answers)
    return lambda prompt: next(iterator)


def silent_output(message):
    """Ignore console output during tests."""
    pass


def test_creates_multiple_processes():
    processes = read_processes(
        input_fn=scripted_reader(
            "2",
            "0", "5", "2",
            "1", "3", "1",
        ),
        output_fn=silent_output,
    )

    assert processes == [
        Process("P1", 0, 5, priority=2),
        Process("P2", 1, 3, priority=1),
    ]


def test_default_priority():
    processes = read_processes(
        input_fn=scripted_reader(
            "1", "0", "3", ""
        ),
        output_fn=silent_output,
    )

    assert processes[0].priority == 1


def test_retries_invalid_process_count():
    messages = []

    processes = read_processes(
        input_fn=scripted_reader(
            "abc", "0", "-1",
            "1", "0", "2", "1",
        ),
        output_fn=messages.append,
    )

    assert len(processes) == 1
    assert any("Invalid value" in m for m in messages)
    assert sum("Value must be >= 1" in m for m in messages) == 2


def test_limits_process_count_to_twenty():
    messages = []

    processes = read_processes(
        input_fn=scripted_reader(
            "21", "1", "0", "2", "1"
        ),
        output_fn=messages.append,
    )

    assert len(processes) == 1
    assert any(
        "Value must be <= 20" in m for m in messages
    )


def test_retries_invalid_arrival_time():
    messages = []

    processes = read_processes(
        input_fn=scripted_reader(
            "1", "-1", "abc", "0", "3", "1"
        ),
        output_fn=messages.append,
    )

    assert processes[0].arrival_time == 0
    assert any("Invalid value" in m for m in messages)


def test_retries_invalid_burst_time():
    processes = read_processes(
        input_fn=scripted_reader(
            "1", "0", "0", "-4", "2", "1"
        ),
        output_fn=silent_output,
    )

    assert processes[0].burst_time == 2


def test_retries_invalid_priority():
    processes = read_processes(
        input_fn=scripted_reader(
            "1", "0", "3", "abc", "0", "2"
        ),
        output_fn=silent_output,
    )

    assert processes[0].priority == 2


def test_accepts_whitespace_around_numbers():
    processes = read_processes(
        input_fn=scripted_reader(
            " 1 ", " 2 ", " 3 ", " 4 "
        ),
        output_fn=silent_output,
    )

    assert processes == [
        Process("P1", 2, 3, priority=4)
    ]


def test_eof_propagates_for_menu_handling():
    answers = iter(["1", "0"])

    def reader(prompt):
        try:
            return next(answers)
        except StopIteration:
            raise EOFError from None

    with pytest.raises(EOFError):
        read_processes(
            input_fn=reader,
            output_fn=silent_output,
        )


def test_created_processes_work_with_all_schedulers():
    processes = read_processes(
        input_fn=scripted_reader(
            "3",
            "0", "5", "3",
            "1", "3", "1",
            "2", "1", "2",
        ),
        output_fn=silent_output,
    )

    schedulers = (
        lambda: schedule_fcfs(processes),
        lambda: schedule_sjf(processes),
        lambda: schedule_rr(processes, quantum=2),
        lambda: schedule_priority(processes),
    )

    for run_scheduler in schedulers:
        results, gantt = run_scheduler()

        assert len(results) == 3
        assert {result.pid for result in results} == {
            "P1", "P2", "P3"
        }

        busy_time = sum(
            segment.duration
            for segment in gantt
            if segment.pid is not None
        )

        assert busy_time == 9
