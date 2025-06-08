import subprocess
import shlex
import os
from typing import Set
from diag_shell.output import print_kv, print_table, print_warning, print_error


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
            "proc": self.cmd_proc,
            "help": self.cmd_help,
        }
        self.env = {"LANG": "C", "LC_ALL": "C", **os.environ}

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
                handler(args)
            except Exception as e:
                print_error(f"[ERROR] {e}")
        else:
            print_error(f"Unknown command: {cmd}. Type 'help' for a list of commands.")

    def get_keywords(self) -> Set[str]:
        return set(self.commands)

    def cmd_cpu(self, args):
        """Display CPU load (1, 5, 15 min averages)."""
        try:
            output = subprocess.check_output(["uptime"], text=True, env=self.env).strip()
            if "load average" in output:
                raw = output.split("load average:")[-1]
                parts = [s.strip().replace(",", ".") for s in raw.split(",")]
                values = [f"{float(p):.2f}" for p in parts[:3]]
                print_kv({
                    "Last 1 min": values[0],
                    "Last 5 min": values[1],
                    "Last 15 min": values[2],
                }, title="CPU Load")
            else:
                print(output)
        except Exception as e:
            print_error(f"[cpu] Failed: {e}")

    def cmd_mem(self, args):
        """Display memory usage."""
        try:
            output = subprocess.check_output(["free", "-h"], text=True, env=self.env).strip().splitlines()
            if len(output) < 2:
                raise ValueError("Unexpected output from 'free -h'")

            raw_headers = output[0].split()
            headers = ["Type"] + raw_headers
            data_lines = output[1:]
            rows = []

            for line in data_lines:
                parts = line.split()
                if not parts:
                    continue
                label = parts[0].rstrip(":")
                values = parts[1:]
                values += ["-"] * (len(raw_headers) - len(values))
                rows.append([label] + values)

            print_table(headers, rows, title="Memory Usage")
        except Exception as e:
            print_error(f"[mem] Failed: {e}")

    def cmd_disk(self, args):
        """Display disk usage."""
        try:
            result = subprocess.run(
                ["df", "-h", "--total"],
                capture_output=True,
                text=True,
                env=self.env
            )
            if result.stdout:
                lines = result.stdout.strip().splitlines()
                headers = lines[0].split()
                rows = [line.split(None, len(headers) - 1) for line in lines[1:]]
                print_table(headers, rows, title="Disk Usage")
            if result.stderr:
                print_warning(result.stderr.strip())
            if result.returncode != 0:
                print_warning(f"Partial failure (exit code {result.returncode})")
        except Exception as e:
            print_error(f"[disk] Failed: {e}")

    def cmd_net(self, args):
        """Display network interfaces."""
        try:
            output = subprocess.check_output(["ip", "-brief", "addr"], text=True, env=self.env).strip()
            print(output)
        except Exception as e:
            print_error(f"[net] Failed: {e}")

    def cmd_uptime(self, args):
        """Display system uptime."""
        try:
            output = subprocess.check_output(["uptime", "-p"], text=True, env=self.env).strip()
            print_kv({"Uptime": output}, title="System Uptime")
        except Exception as e:
            print_error(f"[uptime] Failed: {e}")

    def cmd_proc(self, args):
        """
        Display running processes with optional keyword filtering.

        Usage:
          proc                          Show all processes (like ps aux)
          proc <kw1> <kw2> ...          Show lines matching all keywords (AND logic)
          proc --or <kw1> <kw2> ...     Show lines matching any keyword (OR logic)

        Options:
          --or       Match lines with any of the provided keywords

        Notes:
        - Keywords are case-insensitive.
        - If no result appears, try fewer or alternative keywords.
        - Default logic is AND (all keywords must match)
        """
        try:
            output = subprocess.check_output(["ps", "aux"], text=True, env=self.env).splitlines()
            header = output[0]
            body = output[1:]
            mode = "and"

            if args and args[0] == "--or":
                mode = "or"
                keywords = [kw.lower() for kw in args[1:]]
            else:
                keywords = [kw.lower() for kw in args]

            if keywords:
                if mode == "and":
                    filtered = [line for line in body if all(kw in line.lower() for kw in keywords)]
                elif mode == "or":
                    filtered = [line for line in body if any(kw in line.lower() for kw in keywords)]
            else:
                filtered = body

            print(header)
            print("\n".join(filtered))
        except Exception as e:
            print_error(f"[proc] Failed: {e}")

    def cmd_help(self, args):
        """
        List available commands, or show help for a specific command.

        Usage:
          help              List all commands
          help <command>    Show help for a specific command
        """
        if not args:
            print("Available commands:")
            for cmd in sorted(self.commands):
                doc = self.commands[cmd].__doc__ or ""
                first = doc.strip().split("\n")[0]
                print(f"  {cmd:<10} - {first.strip()}")
        else:
            for cmd in args:
                if cmd in self.commands:
                    print(f"Help for command '{cmd}':\n")
                    print(self.commands[cmd].__doc__ or "(No documentation)\n")
                else:
                    print_error(f"Unknown command: {cmd}")
