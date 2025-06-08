import pytest
import subprocess
from diag_shell.commands.proc import proc


def test_proc_and(monkeypatch, capsys):
    mock_output = """USER PID %CPU COMMAND
serge 123 0.0 python app.py
serge 124 0.0 bash run.sh
serge 125 0.0 bash python test.py"""
    monkeypatch.setattr(subprocess, "check_output", lambda *a, **kw: mock_output)
    proc(interpreter=MockInterpreter(), args=["bash", "python"])
    out = capsys.readouterr().out
    assert "bash python test.py" in out


def test_proc_or(monkeypatch, capsys):
    mock_output = """USER PID %CPU COMMAND
serge 123 0.0 python app.py
serge 124 0.0 bash run.sh
serge 125 0.0 sshd"""
    monkeypatch.setattr(subprocess, "check_output", lambda *a, **kw: mock_output)
    proc(interpreter=MockInterpreter(), args=["--or", "bash", "sshd"])
    out = capsys.readouterr().out
    assert "bash run.sh" in out
    assert "sshd" in out


class MockInterpreter:
    env = {}
