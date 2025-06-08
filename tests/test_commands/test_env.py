import pytest
import subprocess
from diag_shell.commands.env import env


def test_env_output(monkeypatch, capsys):
    mock_output = "USER=serge\nPATH=/usr/bin"
    monkeypatch.setattr(subprocess, "check_output", lambda *a, **kw: mock_output)
    env(interpreter=MockInterpreter(), args=[])
    out = capsys.readouterr().out
    assert "USER=serge" in out
    assert "PATH=" in out


class MockInterpreter:
    env = {}
