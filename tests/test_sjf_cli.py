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


def test_direct_sjf_demo():
    result = run_esinos("--demo-sjf")

    assert result.returncode == 0
    assert "CPU SCHEDULING | SJF" in result.stdout
    assert "PROCESS RESULTS" in result.stdout
    assert "CPU GANTT" in result.stdout
    assert "SCHEDULING SUMMARY" in result.stdout
    assert "Average Waiting Time: 2.67" in result.stdout
    assert "Average Turnaround Time: 5.67" in result.stdout
    assert "MAIN MENU" not in result.stdout


def test_interactive_sjf_demo():
    result = run_esinos(user_input="2\n0\n")

    assert result.returncode == 0
    assert "MAIN MENU" in result.stdout
    assert "CPU SCHEDULING | SJF" in result.stdout
    assert "Exiting ESINOS." in result.stdout


def test_fcfs_and_sjf_in_same_session():
    result = run_esinos(user_input="1\n2\n0\n")

    assert result.returncode == 0
    assert "CPU SCHEDULING | FCFS" in result.stdout
    assert "CPU SCHEDULING | SJF" in result.stdout
    assert "Average Waiting Time: 3.33" in result.stdout
    assert "Average Waiting Time: 2.67" in result.stdout


def test_cli_help_lists_both_algorithms():
    result = run_esinos("--help")

    assert result.returncode == 0
    assert "--demo-fcfs" in result.stdout
    assert "--demo-sjf" in result.stdout


def test_conflicting_demo_options_are_rejected():
    result = run_esinos(
        "--demo-fcfs",
        "--demo-sjf",
    )

    assert result.returncode != 0
    assert "error:" in result.stderr.lower()
