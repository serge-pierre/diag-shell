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


def test_proc_grep(monkeypatch, capsys):
    mock_output = """USER PID %CPU COMMAND
serge 123 0.0 python app.py
serge 124 0.0 bash run.sh"""
    monkeypatch.setattr(subprocess, "check_output", lambda *a, **kw: mock_output)
    proc(interpreter=MockInterpreter(), args=["--grep", "bash"])
    out = capsys.readouterr().out
    assert "bash run.sh" in out
    assert "python" not in out


def test_proc_limit(monkeypatch, capsys):
    mock_output = "USER PID %CPU COMMAND\n" + "\n".join([
        f"serge {100+i} 0.0 cmd{i}" for i in range(10)
    ])
    monkeypatch.setattr(subprocess, "check_output", lambda *a, **kw: mock_output)
    proc(interpreter=MockInterpreter(), args=["--limit", "3"])
    out = capsys.readouterr().out
    assert out.count("serge") == 3


def test_proc_json(monkeypatch, capsys):
    mock_output = """USER PID %CPU COMMAND
serge 101 0.1 python script.py
serge 102 0.2 bash run.sh"""
    monkeypatch.setattr(subprocess, "check_output", lambda *a, **kw: mock_output)
    proc(interpreter=MockInterpreter(), args=["--json"])
    out = capsys.readouterr().out
    assert "\"USER\"" in out
    assert "python" in out
    assert "bash" in out


def test_proc_limit_invalid(monkeypatch, capsys):
    mock_output = "USER PID %CPU COMMAND\nserge 1000 90.0 process_a"
    monkeypatch.setattr(subprocess, "check_output", lambda *a, **kw: mock_output)
    proc(interpreter=MockInterpreter(), args=["--limit", "-1"])
    out = capsys.readouterr().out
    assert "--limit must be a positive integer" in out


def test_proc_or_without_keywords(monkeypatch, capsys):
    mock_output = "USER PID %CPU COMMAND\nserge 1000 90.0 process_a"
    monkeypatch.setattr(subprocess, "check_output", lambda *a, **kw: mock_output)
    proc(interpreter=MockInterpreter(), args=["--or"])
    out = capsys.readouterr().out
    assert "--or requires at least one keyword" in out


class MockInterpreter:
    env = {}
