import pytest
import subprocess
from diag_shell.commands.mem import mem


def test_mem_output(monkeypatch, capsys):
    mem_output = (
        "total used free shared buff/cache available\n"
        "Mem: 8Gi 2Gi 4Gi 1Gi 2Gi 3Gi\n"
        "Swap: 2Gi 1Gi 1Gi"
    )
    monkeypatch.setattr(subprocess, "check_output", lambda *a, **kw: mem_output)
    mem(interpreter=MockInterpreter(), args=[])
    out = capsys.readouterr().out
    assert "Memory Usage" in out
    assert "Mem" in out
    assert "Swap" in out


class MockInterpreter:
    env = {}
