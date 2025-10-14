from subprocess import run, PIPE
import sys


def test_cli_help():
    proc = run([sys.executable, "-m", "necsifactory.cli", "--help"], stdout=PIPE, stderr=PIPE)
    assert proc.returncode == 0
    assert b"NECSI Content Foundry CLI" in proc.stdout
