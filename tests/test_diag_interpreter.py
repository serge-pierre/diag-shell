import pytest
from diag_shell.diag_interpreter import DiagSystemInterpreter
import subprocess


def mock_subprocess_run_success(*args, **kwargs):
    class Result:
        def __init__(self):
            self.stdout = "mock output"
            self.stderr = ""
            self.returncode = 0
    return Result()


def mock_subprocess_run_partial_fail(*args, **kwargs):
    class Result:
        def __init__(self):
            self.stdout = "partial output"
            self.stderr = "df: permission denied"
            self.returncode = 1
    return Result()


def test_keywords():
    interp = DiagSystemInterpreter()
    keywords = interp.get_keywords()
    expected = {"cpu", "mem", "disk", "net", "uptime", "help", "proc"}
    assert expected <= keywords


def test_eval_unknown_command(capsys):
    interp = DiagSystemInterpreter()
    interp.eval("unknown")
    captured = capsys.readouterr()
    assert "Unknown command" in captured.out


@pytest.mark.parametrize("command", ["net", "uptime"])
def test_eval_basic_commands(monkeypatch, capsys, command):
    monkeypatch.setattr(subprocess, "check_output", lambda *a, **kw: "mocked output\n")
    interp = DiagSystemInterpreter()
    interp.eval(command)
    out = capsys.readouterr().out
    assert "mocked output" in out


def test_disk_partial_failure(monkeypatch, capsys):
    monkeypatch.setattr(subprocess, "run", mock_subprocess_run_partial_fail)
    interp = DiagSystemInterpreter()
    interp.eval("disk")
    out = capsys.readouterr().out
    assert "partial" in out
    assert "output" in out
    assert "Partial failure" in out
    assert "Partial failure" in out
    assert "permission denied" in out


def test_disk_success(monkeypatch, capsys):
    monkeypatch.setattr(subprocess, "run", mock_subprocess_run_success)
    interp = DiagSystemInterpreter()
    interp.eval("disk")
    out = capsys.readouterr().out
    assert "mock" in out
    assert "output" in out



def test_cpu_output(monkeypatch, capsys):
    monkeypatch.setattr(subprocess, "check_output", lambda *a, **kw: "load average: 1.23, 0.56, 0.78")
    interp = DiagSystemInterpreter()
    interp.eval("cpu")
    out = capsys.readouterr().out
    assert "Last 1 min" in out
    assert "1.23" in out


def test_mem_output(monkeypatch, capsys):
    mem_output = (
        "total used free shared buff/cache available\n"
        "Mem: 8Gi 2Gi 4Gi 1Gi 2Gi 3Gi\n"
        "Swap: 2Gi 1Gi 1Gi"
    )
    monkeypatch.setattr(subprocess, "check_output", lambda *a, **kw: mem_output)
    interp = DiagSystemInterpreter()
    interp.eval("mem")
    out = capsys.readouterr().out
    assert "Memory Usage" in out
    assert "Mem" in out
    assert "Swap" in out


def test_proc_and(monkeypatch, capsys):
    mock_output = """USER PID %CPU COMMAND
user 123 0.1 bash script.py
user 124 0.2 python script.py
user 125 0.3 bash python replkit"""
    monkeypatch.setattr(subprocess, "check_output", lambda *a, **kw: mock_output)
    interp = DiagSystemInterpreter()
    interp.eval("proc bash python")
    out = capsys.readouterr().out
    assert "bash python replkit" in out
    assert "script.py" not in out


def test_proc_or(monkeypatch, capsys):
    mock_output = """USER PID %CPU COMMAND
user 123 0.1 bash script.py
user 124 0.2 python script.py
user 125 0.3 zsh"""
    monkeypatch.setattr(subprocess, "check_output", lambda *a, **kw: mock_output)
    interp = DiagSystemInterpreter()
    interp.eval("proc --or bash python")
    out = capsys.readouterr().out
    assert "bash script.py" in out
    assert "python script.py" in out
    assert "zsh" not in out
