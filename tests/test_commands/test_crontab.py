import pytest
import subprocess
from diag_shell.commands.crontab import crontab


def test_crontab_entries(monkeypatch, capsys):
    mock_output = "0 5 * * * /usr/bin/python3 /home/serge/backup.py"
    monkeypatch.setattr(subprocess, "check_output", lambda *a, **kw: mock_output)
    crontab(interpreter=MockInterpreter(), args=[])
    out = capsys.readouterr().out
    assert "/usr/bin/python3" in out
    assert "backup.py" in out


def test_crontab_none(monkeypatch, capsys):
    def raise_cpe(*a, **kw):
        raise subprocess.CalledProcessError(returncode=1, cmd=a)
    monkeypatch.setattr(subprocess, "check_output", raise_cpe)
    crontab(interpreter=MockInterpreter(), args=[])
    out = capsys.readouterr().out
    assert "no crontab" in out


class MockInterpreter:
    env = {}
