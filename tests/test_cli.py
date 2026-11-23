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


def test_direct_fcfs_demo():
    result = run_esinos("--demo-fcfs")

    assert result.returncode == 0
    assert "CPU SCHEDULING | FCFS" in result.stdout
    assert "PROCESS RESULTS" in result.stdout
    assert "CPU GANTT" in result.stdout
    assert "SCHEDULING SUMMARY" in result.stdout


def test_interactive_fcfs_demo():
    result = run_esinos(user_input="1\n0\n")

    assert result.returncode == 0
    assert "MAIN MENU" in result.stdout
    assert "CPU SCHEDULING | FCFS" in result.stdout
    assert "Exiting ESINOS." in result.stdout


def test_invalid_menu_option():
    result = run_esinos(user_input="invalid\n0\n")

    assert result.returncode == 0
    assert "Invalid option" in result.stdout


def test_menu_exit():
    result = run_esinos(user_input="0\n")

    assert result.returncode == 0
    assert "Exiting ESINOS." in result.stdout
    assert "PROCESS RESULTS" not in result.stdout
