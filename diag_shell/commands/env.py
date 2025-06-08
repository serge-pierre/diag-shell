from diag_shell.output import print_error
from diag_shell.utils.args import parse_args
import subprocess
import json


def env(interpreter, args):
    """
    Display environment variables.

    Options:
      --grep <pattern>   Filter by keyword
      --json             Output as JSON
    """
    try:
        parsed = parse_args(args, flags={"--json"}, options={"--grep"})
        grep = parsed.get("--grep")
        output = subprocess.check_output(["env"], text=True, env=interpreter.env).strip().splitlines()

        if grep:
            output = [line for line in output if grep in line]

        if parsed.get("--json"):
            as_dict = {}
            for line in output:
                if "=" in line:
                    k, v = line.split("=", 1)
                    as_dict[k] = v
            print(json.dumps(as_dict, indent=2))
        else:
            print("\n".join(output))
    except Exception as e:
        print_error(f"[env] Failed: {e}")
