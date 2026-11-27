from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "code" / "main.py"


def run_esinos(*arguments, user_input=None):
    return subprocess.run(
        [sys.executable, str(MAIN), *arguments],
        input=user_input,
        capture_output=True,
        text=True,
        timeout=5,
        check=False,
    )


def test_direct_rr_quantum_three():
    result = run_esinos("--demo-rr", "--quantum", "3")

    assert result.returncode == 0
    assert "Time quantum: 3" in result.stdout
    assert "CPU SCHEDULING | RR" in result.stdout
    assert "PROCESS RESULTS" in result.stdout
    assert "CPU GANTT" in result.stdout
    assert "SCHEDULING SUMMARY" in result.stdout
    assert "Average Response Time: 2.00" in result.stdout
    assert "MAIN MENU" not in result.stdout


def test_direct_rr_quantum_two():
    result = run_esinos("--demo-rr", "--quantum", "2")

    assert result.returncode == 0
    assert "Time quantum: 2" in result.stdout
    assert "Average Waiting Time: 3.33" in result.stdout
    assert "Average Turnaround Time: 6.33" in result.stdout
    assert "Average Response Time: 1.00" in result.stdout


def test_interactive_rr_custom_quantum():
    result = run_esinos(user_input="4\n2\n0\n")

    assert result.returncode == 0
    assert "[4] CPU Scheduling - Round Robin" in result.stdout
    assert "Time quantum: 2" in result.stdout
    assert "CPU SCHEDULING | RR" in result.stdout
    assert "Exiting ESINOS." in result.stdout


def test_interactive_rr_default_quantum():
    result = run_esinos(user_input="4\n\n0\n")

    assert result.returncode == 0
    assert "Time quantum: 3" in result.stdout
    assert "Exiting ESINOS." in result.stdout


def test_menu_rejects_invalid_quantum():
    result = run_esinos(
        user_input="4\n0\n4\nabc\n0\n"
    )

    assert result.returncode == 0
    assert result.stdout.count("Invalid quantum") == 2
    assert "CPU SCHEDULING | RR" not in result.stdout
    assert "Exiting ESINOS." in result.stdout


def test_cli_rejects_invalid_quantum():
    for value in ("0", "-1", "abc"):
        result = run_esinos(
            "--demo-rr",
            "--quantum",
            value,
        )

        assert result.returncode != 0
        assert "error:" in result.stderr.lower()

    result = run_esinos("--quantum", "3")

    assert result.returncode != 0
    assert "requires --demo-rr" in result.stderr


def test_previous_menu_features_still_work():
    result = run_esinos(
        user_input="1\n2\n3\n0\n"
    )

    assert result.returncode == 0
    assert "CPU SCHEDULING | FCFS" in result.stdout
    assert "CPU SCHEDULING | SJF" in result.stdout
    assert "FCFS VS SJF COMPARISON" in result.stdout
    assert "Exiting ESINOS." in result.stdout


def test_help_and_exclusive_modes():
    help_result = run_esinos("--help")

    assert help_result.returncode == 0
    assert "--demo-fcfs" in help_result.stdout
    assert "--demo-sjf" in help_result.stdout
    assert "--compare-fcfs-sjf" in help_result.stdout
    assert "--demo-rr" in help_result.stdout
    assert "--quantum" in help_result.stdout

    conflict = run_esinos(
        "--demo-rr",
        "--demo-fcfs",
    )

    assert conflict.returncode != 0
    assert "error:" in conflict.stderr.lower()
