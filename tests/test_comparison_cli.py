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


def test_direct_comparison():
    result = run_esinos("--compare-fcfs-sjf")

    assert result.returncode == 0
    assert "FCFS VS SJF COMPARISON" in result.stdout
    assert "Average WT improvement with SJF: 20.00%" in result.stdout
    assert "Best average WT: SJF" in result.stdout
    assert "MAIN MENU" not in result.stdout


def test_interactive_comparison():
    result = run_esinos(user_input="3\n0\n")

    assert result.returncode == 0
    assert "[3] Compare FCFS vs SJF" in result.stdout
    assert "FCFS VS SJF COMPARISON" in result.stdout
    assert "Exiting ESINOS." in result.stdout


def test_all_three_menu_options():
    result = run_esinos(user_input="1\n2\n3\n0\n")

    assert result.returncode == 0
    assert "CPU SCHEDULING | FCFS" in result.stdout
    assert "CPU SCHEDULING | SJF" in result.stdout
    assert "FCFS VS SJF COMPARISON" in result.stdout


def test_help_includes_comparison_option():
    result = run_esinos("--help")

    assert result.returncode == 0
    assert "--demo-fcfs" in result.stdout
    assert "--demo-sjf" in result.stdout
    assert "--compare-fcfs-sjf" in result.stdout


def test_comparison_conflicts_with_other_demos():
    result = run_esinos(
        "--compare-fcfs-sjf",
        "--demo-sjf",
    )

    assert result.returncode != 0
    assert "error:" in result.stderr.lower()
