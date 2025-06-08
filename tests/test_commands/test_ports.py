import pytest
import subprocess
from diag_shell.commands.ports import ports


def test_ports_output(monkeypatch, capsys):
    mock_output = (
        "Netid State      Recv-Q Send-Q Local Address:Port               Peer Address:Port\n"
        "tcp   LISTEN     0      128    127.0.0.1:22                  0.0.0.0:*"
    )
    monkeypatch.setattr(subprocess, "check_output", lambda *a, **kw: mock_output)
    ports(interpreter=MockInterpreter(), args=[])
    out = capsys.readouterr().out
    assert "127.0.0.1:22" in out
    assert "LISTEN" in out


class MockInterpreter:
    env = {}
