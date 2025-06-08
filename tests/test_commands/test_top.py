import pytest
import subprocess
from diag_shell.commands.top import top


def test_top_output(monkeypatch, capsys):
    mock_output = (
        "USER PID %CPU COMMAND\n"
        "serge 1000 90.0 process_a\n"
        "serge 1001 80.0 process_b\n"
        "serge 1002 70.0 process_c\n"
        "serge 1003 60.0 process_d\n"
        "serge 1004 50.0 process_e\n"
        "serge 1005 40.0 process_f"
    )
    monkeypatch.setattr(subprocess, "check_output", lambda *a, **kw: mock_output)
    top(interpreter=MockInterpreter(), args=["--limit", "5"])
    out = capsys.readouterr().out
    assert "process_f" not in out


def test_top_json(monkeypatch, capsys):
    mock_output = (
        "USER PID %CPU COMMAND\n"
        "serge 1000 90.0 process_a\n"
        "serge 1001 80.0 process_b"
    )
    monkeypatch.setattr(subprocess, "check_output", lambda *a, **kw: mock_output)
    top(interpreter=MockInterpreter(), args=["--json"])
    out = capsys.readouterr().out
    assert "\"USER\"" in out
    assert "process_a" in out


def test_top_limit_invalid(monkeypatch, capsys):
    mock_output = "USER PID %CPU COMMAND\nserge 1000 90.0 process_a"
    monkeypatch.setattr(subprocess, "check_output", lambda *a, **kw: mock_output)
    top(interpreter=MockInterpreter(), args=["--limit", "0"])
    out = capsys.readouterr().out
    assert "--limit must be a positive integer" in out


class MockInterpreter:
    env = {}
