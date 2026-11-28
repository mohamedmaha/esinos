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


def test_direct_priority_demo():
    result = run_esinos("--demo-priority")

    assert result.returncode == 0
    assert "CPU SCHEDULING | PRIORITY" in result.stdout
    assert "PROCESS RESULTS" in result.stdout
    assert "CPU GANTT" in result.stdout
    assert "SCHEDULING SUMMARY" in result.stdout
    assert "MAIN MENU" not in result.stdout


def test_direct_priority_metrics():
    result = run_esinos("--demo-priority")

    assert result.returncode == 0
    assert "Average Waiting Time: 4.00" in result.stdout
    assert "Average Turnaround Time: 7.25" in result.stdout
    assert "Average Response Time: 4.00" in result.stdout

    assert (
        "Priority rule: lower number = higher priority"
        in result.stdout
    )


def test_interactive_priority_demo():
    result = run_esinos(user_input="6\n0\n")

    assert result.returncode == 0
    assert "[6] CPU Scheduling - Priority Demo" in result.stdout
    assert "CPU SCHEDULING | PRIORITY" in result.stdout
    assert "Exiting ESINOS." in result.stdout


def test_all_scheduling_menu_options():
    result = run_esinos(
        user_input="1\n2\n3\n4\n2\n5\n2\n6\n0\n"
    )

    assert result.returncode == 0
    assert "CPU SCHEDULING | FCFS" in result.stdout
    assert "CPU SCHEDULING | SJF" in result.stdout
    assert "CPU SCHEDULING | RR" in result.stdout
    assert "CPU SCHEDULING | PRIORITY" in result.stdout
    assert "FCFS VS SJF COMPARISON" in result.stdout
    assert "FCFS VS SJF VS ROUND ROBIN" in result.stdout
    assert "Exiting ESINOS." in result.stdout


def test_cli_help_includes_priority():
    result = run_esinos("--help")

    assert result.returncode == 0
    assert "--demo-fcfs" in result.stdout
    assert "--demo-sjf" in result.stdout
    assert "--demo-rr" in result.stdout
    assert "--demo-priority" in result.stdout
    assert "--compare-fcfs-sjf" in result.stdout
    assert "--compare-all" in result.stdout


def test_priority_is_mutually_exclusive():
    result = run_esinos(
        "--demo-priority",
        "--demo-rr",
    )

    assert result.returncode != 0
    assert "error:" in result.stderr.lower()


def test_priority_rejects_quantum_argument():
    result = run_esinos(
        "--demo-priority",
        "--quantum",
        "2",
    )

    assert result.returncode != 0
    assert "error:" in result.stderr.lower()


def test_invalid_menu_choice_then_priority():
    result = run_esinos(
        user_input="7\n6\n0\n"
    )

    assert result.returncode == 0
    assert "Invalid option" in result.stdout
    assert "CPU SCHEDULING | PRIORITY" in result.stdout
    assert "Exiting ESINOS." in result.stdout
