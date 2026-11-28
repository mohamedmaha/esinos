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


def test_custom_four_way_comparison():
    result = run_esinos(
        "7\n3\n"
        "0\n5\n3\n"
        "1\n3\n1\n"
        "2\n1\n2\n"
        "5\n2\n0\n0\n"
    )

    assert result.returncode == 0
    assert (
        "ESINOS - FOUR-WAY SCHEDULING COMPARISON"
        in result.stdout
    )
    assert "RR(q=2)" in result.stdout
    assert "Best average WT: SJF" in result.stdout
    assert "Best average TAT: SJF" in result.stdout
    assert "Best average RT: RR" in result.stdout
    assert "Exiting ESINOS." in result.stdout


def test_custom_comparison_default_quantum():
    result = run_esinos(
        "7\n1\n"
        "0\n3\n1\n"
        "5\n\n0\n0\n"
    )

    assert result.returncode == 0
    assert "RR(q=2)" in result.stdout
    assert (
        "Best average WT: FCFS / SJF / RR / PRIORITY"
        in result.stdout
    )


def test_custom_comparison_quantum_three():
    result = run_esinos(
        "7\n2\n"
        "0\n5\n3\n"
        "1\n3\n1\n"
        "5\n3\n0\n0\n"
    )

    assert result.returncode == 0
    assert "RR(q=3)" in result.stdout
    assert "PERFORMANCE ANALYSIS" in result.stdout


def test_custom_comparison_retries_invalid_quantum():
    result = run_esinos(
        "7\n1\n"
        "0\n3\n1\n"
        "5\n0\nabc\n2\n"
        "0\n0\n"
    )

    assert result.returncode == 0
    assert "Value must be >= 1." in result.stdout
    assert (
        "Invalid value. Enter an integer."
        in result.stdout
    )
    assert "RR(q=2)" in result.stdout


def test_comparison_reuses_existing_processes():
    result = run_esinos(
        "7\n2\n"
        "0\n5\n3\n"
        "1\n3\n1\n"
        "1\n5\n2\n4\n0\n0\n"
    )

    assert result.returncode == 0
    assert "CPU SCHEDULING | FCFS" in result.stdout
    assert (
        "ESINOS - FOUR-WAY SCHEDULING COMPARISON"
        in result.stdout
    )
    assert "CPU SCHEDULING | PRIORITY" in result.stdout

    assert result.stdout.count(
        "2 processes created successfully."
    ) == 1


def test_custom_comparison_uses_priorities():
    result = run_esinos(
        "7\n3\n"
        "0\n8\n3\n"
        "0\n4\n2\n"
        "0\n1\n1\n"
        "5\n2\n0\n0\n"
    )

    assert result.returncode == 0
    assert (
        "PRIORITY: P3 -> P2 -> P1"
        in result.stdout
    )
    assert "FCFS: P1 -> P2 -> P3" in result.stdout


def test_back_to_main_menu_preserves_old_demos():
    result = run_esinos(
        "7\n1\n"
        "0\n3\n1\n"
        "0\n1\n0\n"
    )

    assert result.returncode == 0
    assert "Returning to main menu." in result.stdout
    assert "CPU SCHEDULING | FCFS" in result.stdout
    assert "Exiting ESINOS." in result.stdout


def test_custom_comparison_eof_handling():
    result = run_esinos(
        "7\n1\n"
        "0\n3\n1\n"
        "5\n"
    )

    assert result.returncode == 0
    assert "Returning to main menu." in result.stdout
    assert "Exiting ESINOS." in result.stdout
