from diag_shell.output import print_error
from diag_shell.utils.args import parse_args
import subprocess
import json


def crontab(interpreter, args):
    """
    Display the current user's crontab entries.

    Options:
      --grep <pattern>   Filter lines containing <pattern>
      --json             Output in JSON format (line by line)
    """
    try:
        parsed = parse_args(args, flags={"--json"}, options={"--grep"})
        grep = parsed.get("--grep")
        json_mode = parsed.get("--json", False)

        result = subprocess.run(
            ["crontab", "-l"], capture_output=True, text=True, env=interpreter.env
        )

        lines = result.stdout.strip().splitlines()

        if grep:
            lines = [line for line in lines if grep in line]

        if json_mode:
            data = [{"line": line} for line in lines]
            print(json.dumps(data, indent=2))
        else:
            print("== Crontab ==")
            print("\n".join(lines))

        if result.returncode != 0 and result.stderr:
            print_error(f"[crontab] Warning: {result.stderr.strip()}")

    except Exception as e:
        print_error(f"[crontab] Failed: {e}")
