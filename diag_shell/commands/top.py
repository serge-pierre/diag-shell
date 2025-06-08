from diag_shell.output import print_error
from diag_shell.utils.args import parse_args
import subprocess
import json


def top(interpreter, args):
    """
    Display top CPU-consuming processes.

    Options:
      --limit <n>       Limit number of processes shown
      --grep <pattern>  Filter lines containing pattern
      --json            Output as JSON
    """
    try:
        parsed = parse_args(args, flags={"--json"}, options={"--limit", "--grep"})
        limit = parsed.get("--limit")
        grep = parsed.get("--grep")
        json_mode = parsed.get("--json", False)

        if limit is not None:
            try:
                limit = int(limit)
                if limit < 1:
                    raise ValueError("--limit must be a positive integer")
            except ValueError:
                raise ValueError("--limit must be a positive integer")

        output = subprocess.check_output(["ps", "aux", "--sort=-%cpu"], text=True, env=interpreter.env).strip().splitlines()
        header, *lines = output

        if grep:
            lines = [line for line in lines if grep in line]

        if limit:
            lines = lines[:limit]

        if json_mode:
            cols = header.split()
            structured = []
            for line in lines:
                parts = line.split(None, len(cols) - 1)
                if len(parts) == len(cols):
                    structured.append(dict(zip(cols, parts)))
            print(json.dumps(structured, indent=2))
        else:
            print(header)
            print("\n".join(lines))

    except Exception as e:
        print_error(f"[top] Failed: {e}")
