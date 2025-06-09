import pytest
import subprocess
from diag_shell.commands.disk import disk


def test_disk_output(monkeypatch, capsys):
    mock_output = """Filesystem      Size  Used Avail Use% Mounted on
/dev/loop0       111M  111M     0  100% /snap/core18/2855
/dev/loop1       56M   56M      0  100% /snap/core20/1822"""
    monkeypatch.setattr(subprocess, "run", lambda *a, **kw: subprocess.CompletedProcess(a[0], 0, mock_output, ""))
    disk(interpreter=MockInterpreter(), args=[])
    out = capsys.readouterr().out
    assert "Disk Usage" in out
    assert "/dev/loop0" in out


def test_disk_grep(monkeypatch, capsys):
    mock_output = """Filesystem      Size  Used Avail Use% Mounted on
/dev/loop0       111M  111M     0  100% /snap/core18/2855
/dev/loop1       56M   56M      0  100% /snap/core20/1822"""
    monkeypatch.setattr(subprocess, "run", lambda *a, **kw: subprocess.CompletedProcess(a[0], 0, mock_output, ""))
    disk(interpreter=MockInterpreter(), args=["--grep", "core20"])
    out = capsys.readouterr().out
    assert "/snap/core20/1822" in out
    assert "/snap/core18/2855" not in out


def test_disk_json(monkeypatch, capsys):
    mock_output = """Filesystem      Size  Used Avail Use% Mounted on
/dev/loop0       111M  111M     0  100% /snap/core18/2855"""
    monkeypatch.setattr(subprocess, "run", lambda *a, **kw: subprocess.CompletedProcess(a[0], 0, mock_output, ""))
    disk(interpreter=MockInterpreter(), args=["--json"])
    out = capsys.readouterr().out
    assert "\"Filesystem\"" in out
    assert "/snap/core18/2855" in out
    assert "Mounted on" in out


class MockInterpreter:
    env = {}
