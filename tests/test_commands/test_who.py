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


class MockInterpreter:
    env = {}
