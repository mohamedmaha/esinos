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


def test_direct_three_way_default_quantum():
    result = run_esinos("--compare-all")

    assert result.returncode == 0
    assert "FCFS VS SJF VS ROUND ROBIN" in result.stdout
    assert "RR(q=2)" in result.stdout
    assert "Best average WT: SJF" in result.stdout
    assert "Best average RT: RR" in result.stdout
    assert "MAIN MENU" not in result.stdout


def test_direct_three_way_custom_quantum():
    result = run_esinos(
        "--compare-all",
        "--quantum",
        "3",
    )

    assert result.returncode == 0
    assert "RR(q=3)" in result.stdout
    assert "FCFS VS SJF VS ROUND ROBIN" in result.stdout


def test_interactive_comparison_default_quantum():
    result = run_esinos(user_input="5\n\n0\n")

    assert result.returncode == 0
    assert "[5] Compare FCFS vs SJF vs RR" in result.stdout
    assert "RR(q=2)" in result.stdout
    assert "Exiting ESINOS." in result.stdout


def test_interactive_comparison_custom_quantum():
    result = run_esinos(user_input="5\n3\n0\n")

    assert result.returncode == 0
    assert "RR(q=3)" in result.stdout
    assert "Exiting ESINOS." in result.stdout


def test_interactive_rejects_invalid_quantum():
    result = run_esinos(
        user_input="5\n0\n5\nabc\n0\n"
    )

    assert result.returncode == 0
    assert result.stdout.count("Invalid quantum") == 2
    assert "FCFS VS SJF VS ROUND ROBIN" not in result.stdout
    assert "Exiting ESINOS." in result.stdout


def test_cli_rejects_invalid_quantum_usage():
    for value in ("0", "-2", "abc"):
        result = run_esinos(
            "--compare-all",
            "--quantum",
            value,
        )

        assert result.returncode != 0
        assert "error:" in result.stderr.lower()

    no_mode = run_esinos("--quantum", "2")

    assert no_mode.returncode != 0
    assert "requires --demo-rr" in no_mode.stderr

    wrong_mode = run_esinos(
        "--demo-fcfs",
        "--quantum",
        "2",
    )

    assert wrong_mode.returncode != 0


def test_previous_features_still_work():
    result = run_esinos(
        user_input="1\n2\n3\n4\n2\n0\n"
    )

    assert result.returncode == 0
    assert "CPU SCHEDULING | FCFS" in result.stdout
    assert "CPU SCHEDULING | SJF" in result.stdout
    assert "FCFS VS SJF COMPARISON" in result.stdout
    assert "CPU SCHEDULING | RR" in result.stdout
    assert "Exiting ESINOS." in result.stdout


def test_help_and_mutually_exclusive_modes():
    help_result = run_esinos("--help")

    assert help_result.returncode == 0
    assert "--demo-fcfs" in help_result.stdout
    assert "--demo-sjf" in help_result.stdout
    assert "--demo-rr" in help_result.stdout
    assert "--compare-fcfs-sjf" in help_result.stdout
    assert "--compare-all" in help_result.stdout

    conflict = run_esinos(
        "--compare-all",
        "--demo-rr",
    )

    assert conflict.returncode != 0
    assert "error:" in conflict.stderr.lower()
