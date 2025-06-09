import pytest
import subprocess
from diag_shell.commands.crontab import crontab


def test_crontab_output(monkeypatch, capsys):
    mock_cron = """# Backup job
0 2 * * * /usr/bin/backup.sh
"""
    monkeypatch.setattr(subprocess, "run", lambda *a, **kw: subprocess.CompletedProcess(a[0], 0, mock_cron, ""))
    crontab(interpreter=MockInterpreter(), args=[])
    out = capsys.readouterr().out
    assert "/usr/bin/backup.sh" in out


def test_crontab_grep(monkeypatch, capsys):
    mock_cron = """# Comment
0 2 * * * /usr/bin/backup.sh
0 3 * * * /usr/bin/clean.sh
"""
    monkeypatch.setattr(subprocess, "run", lambda *a, **kw: subprocess.CompletedProcess(a[0], 0, mock_cron, ""))
    crontab(interpreter=MockInterpreter(), args=["--grep", "clean"])
    out = capsys.readouterr().out
    assert "/usr/bin/clean.sh" in out
    assert "/usr/bin/backup.sh" not in out


def test_crontab_json(monkeypatch, capsys):
    mock_cron = "0 2 * * * /usr/bin/backup.sh"
    monkeypatch.setattr(subprocess, "run", lambda *a, **kw: subprocess.CompletedProcess(a[0], 0, mock_cron, ""))
    crontab(interpreter=MockInterpreter(), args=["--json"])
    out = capsys.readouterr().out
    assert "\"line\"" in out
    assert "/usr/bin/backup.sh" in out


class MockInterpreter:
    env = {}
