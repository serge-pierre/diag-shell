import pytest
from diag_shell.commands.help import help as help_cmd


class MockInterpreter:
    def __init__(self):
        self.commands = {
            "cpu": lambda *_: None,
            "mem": lambda *_: None,
            "proc": lambda *_: None,
        }
        self.commands["cpu"].__doc__ = "Display CPU usage."
        self.commands["mem"].__doc__ = "Display memory usage."
        self.commands["proc"].__doc__ = """Display processes.

Supports filtering with --or.
"""


def test_help_list(capsys):
    help_cmd(MockInterpreter(), [])
    out = capsys.readouterr().out
    assert "Available commands" in out
    assert "cpu" in out
    assert "Display CPU usage" in out


def test_help_specific(capsys):
    help_cmd(MockInterpreter(), ["proc"])
    out = capsys.readouterr().out
    assert "Help for command 'proc'" in out
    assert "Supports filtering" in out


def test_help_unknown(capsys):
    help_cmd(MockInterpreter(), ["xyz"])
    out = capsys.readouterr().out
    assert "Unknown command: xyz" in out
