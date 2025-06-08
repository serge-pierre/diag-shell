import pytest
import subprocess
from diag_shell.commands.cpu import cpu


def test_cpu_output(monkeypatch, capsys):
    monkeypatch.setattr(
        subprocess, "check_output", lambda *a, **kw: "load average: 1.23, 0.56, 0.78"
    )
    cpu(interpreter=MockInterpreter(), args=[])
    out = capsys.readouterr().out
    assert "Last 1 min" in out
    assert "1.23" in out


class MockInterpreter:
    env = {}
