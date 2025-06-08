from diag_shell.output import print_error
from diag_shell.utils.args import parse_args
import subprocess
import json


def who(interpreter, args):
    """
    Display users currently logged in.

    Options:
      --grep <pattern>   Filter by keyword
      --json             Output as JSON
    """
    try:
        parsed = parse_args(args, flags={"--json"}, options={"--grep"})
        grep = parsed.get("--grep")
        output = subprocess.check_output(["who"], text=True, env=interpreter.env).strip().splitlines()

        if grep:
            output = [line for line in output if grep in line]

        if parsed.get("--json"):
            parsed_output = []
            for line in output:
                parts = line.split()
                if len(parts) >= 3:
                    parsed_output.append({
                        "user": parts[0],
                        "tty": parts[1],
                        "since": " ".join(parts[2:]),
                    })
            print(json.dumps(parsed_output, indent=2))
        else:
            print("\n".join(output))
    except Exception as e:
        print_error(f"[who] Failed: {e}")
