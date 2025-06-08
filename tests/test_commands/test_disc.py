import pytest
import subprocess
from diag_shell.commands.disk import disk


def test_disk_output(monkeypatch, capsys):
    output = (
        "Filesystem Size Used Avail Use% Mounted on\n" "/dev/sda1 100G 50G 50G 50% /"
    )

    def mock_run(*args, **kwargs):
        class Result:
            stdout = output
            stderr = ""
            returncode = 0

        return Result()

    monkeypatch.setattr(subprocess, "run", mock_run)
    disk(interpreter=MockInterpreter(), args=[])
    out = capsys.readouterr().out
    assert "Disk Usage" in out
    assert "/dev/sda1" in out


class MockInterpreter:
    env = {}
