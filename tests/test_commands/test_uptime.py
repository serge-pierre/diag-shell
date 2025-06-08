import pytest
import subprocess
from diag_shell.commands.uptime import uptime


def test_uptime_output(monkeypatch, capsys):
    monkeypatch.setattr(
        subprocess, "check_output", lambda *a, **kw: "up 1 hour, 2 minutes"
    )
    uptime(interpreter=MockInterpreter(), args=[])
    out = capsys.readouterr().out
    assert "System Uptime" in out
    assert "1 hour" in out


class MockInterpreter:
    env = {}
