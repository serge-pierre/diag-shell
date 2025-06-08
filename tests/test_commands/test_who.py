import pytest
import subprocess
from diag_shell.commands.who import who


def test_who_output(monkeypatch, capsys):
    mock_output = "serge    tty7    Jun  4 01:07 (:0)"
    monkeypatch.setattr(subprocess, "check_output", lambda *a, **kw: mock_output)
    who(interpreter=MockInterpreter(), args=[])
    out = capsys.readouterr().out
    assert "serge" in out
    assert "tty7" in out


def test_who_grep(monkeypatch, capsys):
    mock_output = "serge    tty1    Jun  4 01:07\nserge    tty2    Jun  4 01:08"
    monkeypatch.setattr(subprocess, "check_output", lambda *a, **kw: mock_output)
    who(interpreter=MockInterpreter(), args=["--grep", "tty2"])
    out = capsys.readouterr().out
    assert "tty2" in out
    assert "tty1" not in out


def test_who_json(monkeypatch, capsys):
    mock_output = "serge    tty1    Jun  4 01:07"
    monkeypatch.setattr(subprocess, "check_output", lambda *a, **kw: mock_output)
    who(interpreter=MockInterpreter(), args=["--json"])
    out = capsys.readouterr().out
    assert "\"user\"" in out
    assert "\"tty\"" in out


def test_who_grep_json(monkeypatch, capsys):
    mock_output = "serge    tty1    Jun  4 01:07\nserge    tty2    Jun  4 01:08"
    monkeypatch.setattr(subprocess, "check_output", lambda *a, **kw: mock_output)
    who(interpreter=MockInterpreter(), args=["--grep", "tty1", "--json"])
    out = capsys.readouterr().out
    assert "tty1" in out
    assert "tty2" not in out


def test_who_unknown_option(monkeypatch, capsys):
    mock_output = "serge tty1 Jun  4 01:07"
    monkeypatch.setattr(subprocess, "check_output", lambda *a, **kw: mock_output)
    who(interpreter=MockInterpreter(), args=["--js"])
    out = capsys.readouterr().out
    assert "Unknown option" in out


class MockInterpreter:
    env = {}
