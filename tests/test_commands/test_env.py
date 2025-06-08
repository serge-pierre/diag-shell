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


def test_env_grep(monkeypatch, capsys):
    mock_output = "USER=serge\nPATH=/usr/bin\nEDITOR=vim"
    monkeypatch.setattr(subprocess, "check_output", lambda *a, **kw: mock_output)
    env(interpreter=MockInterpreter(), args=["--grep", "PATH"])
    out = capsys.readouterr().out
    assert "PATH=" in out
    assert "USER=" not in out


def test_env_json(monkeypatch, capsys):
    mock_output = "USER=serge\nPATH=/usr/bin"
    monkeypatch.setattr(subprocess, "check_output", lambda *a, **kw: mock_output)
    env(interpreter=MockInterpreter(), args=["--json"])
    out = capsys.readouterr().out
    assert "{" in out
    assert "\"PATH\"" in out


def test_env_grep_json(monkeypatch, capsys):
    mock_output = "USER=serge\nPATH=/usr/bin\nTERM=xterm"
    monkeypatch.setattr(subprocess, "check_output", lambda *a, **kw: mock_output)
    env(interpreter=MockInterpreter(), args=["--grep", "TERM", "--json"])
    out = capsys.readouterr().out
    assert "\"TERM\"" in out
    assert "PATH" not in out


class MockInterpreter:
    env = {}
