import subprocess
import shlex
from typing import Set


class DiagSystemInterpreter:
    """
    A system diagnostic interpreter meant to be plugged into replkit.
    Provides simplified commands for querying CPU, memory, disk, network, and system state.
    """

    def __init__(self):
        self.commands = {
            "cpu": self.cmd_cpu,
            "mem": self.cmd_mem,
            "disk": self.cmd_disk,
            "net": self.cmd_net,
            "uptime": self.cmd_uptime,
            "help": self.cmd_help,
        }

    def eval(self, line: str) -> None:
        """
        Evaluate a user-entered command line.
        """
        line = line.strip()
        if not line:
            return

        parts = shlex.split(line)
        cmd = parts[0]
        args = parts[1:]

        handler = self.commands.get(cmd)
        if handler:
            try:
                handler(args)
            except Exception as e:
                print(f"[ERROR] {e}")
        else:
            print(f"Unknown command: {cmd}. Type 'help' for a list of commands.")

    def get_keywords(self) -> Set[str]:
        """
        Return the set of known command keywords for autocompletion.
        """
        return set(self.commands)

    def cmd_cpu(self, args):
        """Display CPU load."""
        try:
            output = subprocess.check_output(["uptime"]).decode()
            print(output.strip())
        except Exception as e:
            print(f"[cpu] Failed: {e}")

    def cmd_mem(self, args):
        """Display memory usage."""
        try:
            output = subprocess.check_output(["free", "-h"]).decode()
            print(output.strip())
        except Exception as e:
            print(f"[mem] Failed: {e}")

    def cmd_disk(self, args):
        """Display disk usage."""
        try:
            result = subprocess.run(
                ["df", "-h", "--total"], capture_output=True, text=True
            )
            if result.stdout:
                print(result.stdout.strip())
            if result.stderr:
                print(f"[disk] Warning: {result.stderr.strip()}")
            if result.returncode != 0:
                print(f"[disk] Partial failure (exit code {result.returncode})")
        except Exception as e:
            print(f"[disk] Failed: {e}")

    def cmd_net(self, args):
        """Display network interfaces."""
        try:
            output = subprocess.check_output(["ip", "-brief", "addr"]).decode()
            print(output.strip())
        except Exception as e:
            print(f"[net] Failed: {e}")

    def cmd_uptime(self, args):
        """Display system uptime."""
        try:
            output = subprocess.check_output(["uptime", "-p"]).decode()
            print(output.strip())
        except Exception as e:
            print(f"[uptime] Failed: {e}")

    def cmd_help(self, args):
        """List available commands."""
        print("Available commands:")
        for cmd in sorted(self.commands):
            doc = self.commands[cmd].__doc__ or ""
            print(f"  {cmd:<10} - {doc.strip()}")
