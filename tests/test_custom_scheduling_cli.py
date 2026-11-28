from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "code" / "main.py"


def run_esinos(user_input):
    return subprocess.run(
        [sys.executable, str(MAIN)],
        input=user_input,
        capture_output=True,
        text=True,
        timeout=5,
        check=False,
    )


def test_custom_fcfs():
    result = run_esinos(
        "7\n2\n"
        "0\n5\n2\n"
        "1\n3\n1\n"
        "1\n0\n0\n"
    )

    assert result.returncode == 0
    assert "2 processes created successfully." in result.stdout
    assert "CPU SCHEDULING | FCFS" in result.stdout
    assert "Returning to main menu." in result.stdout
    assert "Exiting ESINOS." in result.stdout


def test_custom_sjf():
    result = run_esinos(
        "7\n3\n"
        "0\n5\n2\n"
        "1\n3\n1\n"
        "2\n1\n2\n"
        "2\n0\n0\n"
    )

    assert result.returncode == 0
    assert "CPU SCHEDULING | SJF" in result.stdout
    assert "Average Waiting Time: 2.67" in result.stdout


def test_custom_rr_quantum_two():
    result = run_esinos(
        "7\n2\n"
        "0\n5\n2\n"
        "1\n3\n1\n"
        "3\n2\n0\n0\n"
    )

    assert result.returncode == 0
    assert "CPU SCHEDULING | RR" in result.stdout
    assert "Time quantum: 2" in result.stdout
    assert "CPU GANTT" in result.stdout


def test_custom_priority():
    result = run_esinos(
        "7\n2\n"
        "0\n5\n3\n"
        "0\n2\n1\n"
        "4\n0\n0\n"
    )

    assert result.returncode == 0
    assert "CPU SCHEDULING | PRIORITY" in result.stdout
    assert "PROCESS RESULTS" in result.stdout
    assert "SCHEDULING SUMMARY" in result.stdout


def test_all_algorithms_same_custom_session():
    result = run_esinos(
        "7\n2\n"
        "0\n5\n3\n"
        "1\n3\n1\n"
        "1\n2\n3\n2\n4\n0\n0\n"
    )

    assert result.returncode == 0

    assert "CPU SCHEDULING | FCFS" in result.stdout
    assert "CPU SCHEDULING | SJF" in result.stdout
    assert "CPU SCHEDULING | RR" in result.stdout
    assert "CPU SCHEDULING | PRIORITY" in result.stdout

    assert result.stdout.count(
        "2 processes created successfully."
    ) == 1


def test_custom_input_retries_invalid_values():
    result = run_esinos(
        "7\n"
        "0\nabc\n1\n"
        "-1\n0\n"
        "0\n2\n"
        "0\n\n"
        "1\n0\n0\n"
    )

    assert result.returncode == 0
    assert "Invalid value. Enter an integer." in result.stdout
    assert "Value must be >= 1." in result.stdout
    assert "Value must be >= 0." in result.stdout
    assert "CPU SCHEDULING | FCFS" in result.stdout


def test_custom_rr_invalid_quantum_retries():
    result = run_esinos(
        "7\n1\n"
        "0\n3\n1\n"
        "3\n0\nabc\n\n"
        "0\n0\n"
    )

    assert result.returncode == 0
    assert "Value must be >= 1." in result.stdout
    assert "Invalid value. Enter an integer." in result.stdout
    assert "Time quantum: 3" in result.stdout
    assert "CPU SCHEDULING | RR" in result.stdout


def test_custom_eof_is_handled_gracefully():
    result = run_esinos(
        "7\n1\n0\n"
    )

    assert result.returncode == 0
    assert "Returning to main menu." in result.stdout
    assert "Exiting ESINOS." in result.stdout
