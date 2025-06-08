import subprocess
import shlex
import os
from typing import Set
from diag_shell.output import print_error
from diag_shell.commands import register_commands


class DiagSystemInterpreter:
    """
    A system diagnostic interpreter meant to be plugged into replkit.
    Uses a modular registry of command handlers.
    """

    def __init__(self):
        self.commands = {}
        self.env = {"LANG": "C", "LC_ALL": "C", **os.environ}
        register_commands(self)

    def eval(self, line: str) -> None:
        line = line.strip()
        if not line:
            return

        parts = shlex.split(line)
        cmd = parts[0]
        args = parts[1:]

        handler = self.commands.get(cmd)
        if handler:
            try:
                handler(self, args)
            except Exception as e:
                print_error(f"[ERROR] {e}")
        else:
            print_error(f"Unknown command: {cmd}. Type 'help' for a list of commands.")

    def get_keywords(self) -> Set[str]:
        return set(self.commands)
