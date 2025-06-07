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
    expected = {"cpu", "mem", "disk", "net", "uptime", "help"}
    assert expected <= keywords


def test_eval_unknown_command(capsys):
    interp = DiagSystemInterpreter()
    interp.eval("unknown")
    captured = capsys.readouterr()
    assert "Unknown command" in captured.out


@pytest.mark.parametrize("command", ["cpu", "mem", "net", "uptime"])
def test_eval_command_success(monkeypatch, capsys, command):
    monkeypatch.setattr(subprocess, "check_output", lambda *a, **kw: b"mocked output\n")
    interp = DiagSystemInterpreter()
    interp.eval(command)
    captured = capsys.readouterr()
    assert "mocked output" in captured.out


def test_disk_partial_failure(monkeypatch, capsys):
    monkeypatch.setattr(subprocess, "run", mock_subprocess_run_partial_fail)
    interp = DiagSystemInterpreter()
    interp.eval("disk")
    out = capsys.readouterr().out
    assert "partial output" in out
    assert "Partial failure" in out
    assert "permission denied" in out


def test_disk_success(monkeypatch, capsys):
    monkeypatch.setattr(subprocess, "run", mock_subprocess_run_success)
    interp = DiagSystemInterpreter()
    interp.eval("disk")
    out = capsys.readouterr().out
    assert "mock output" in out
    assert "Partial failure" not in out
    assert "Warning" not in out
