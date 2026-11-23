from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def test_esinos_starts_successfully():
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "code" / "main.py"),
            "--help",
        ],
        capture_output=True,
        text=True,
        timeout=5,
        check=False,
    )

    assert result.returncode == 0
    assert "ESINOS" in result.stdout
    assert "--demo-fcfs" in result.stdout
