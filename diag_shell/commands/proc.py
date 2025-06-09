from diag_shell.output import print_error
from diag_shell.utils.args import parse_args
import subprocess
import json


def proc(interpreter, args):
    """
    Display running processes with optional filtering.

    Filtering (keywords):
      - <kw1> <kw2>     : Match all keywords (AND logic, default)
      - --or <kw1> ...  : Match any keyword (OR logic, must be followed by 1+ keywords)
      - --grep <pat>    : Raw line must contain <pat>

    Options:
      --limit <n>       : Limit number of matching lines displayed (must be > 0)
      --json            : Output structured process info in JSON format

    Evaluation order:
      1. Keyword filtering (AND / OR)
      2. --grep filter (raw lines)
      3. --limit
      4. --json formatting

    Example:
      proc ssh python --grep code --limit 5 --json
    """
    try:
        parsed = parse_args(args, flags={"--or", "--json"}, options={"--grep", "--limit"})
        keywords = parsed["args"]
        mode_or = parsed.get("--or", False)
        grep = parsed.get("--grep")
        limit = parsed.get("--limit")
        json_mode = parsed.get("--json", False)

        if mode_or and not keywords:
            raise ValueError("--or requires at least one keyword")

        if limit is not None:
            try:
                limit = int(limit)
                if limit < 1:
                    raise ValueError("--limit must be a positive integer")
            except ValueError:
                raise ValueError("--limit must be a positive integer")

        output = subprocess.check_output(["ps", "aux"], text=True, env=interpreter.env).strip().splitlines()
        header, *lines = output

        if keywords:
            if mode_or:
                lines = [line for line in lines if any(k in line for k in keywords)]
            else:
                lines = [line for line in lines if all(k in line for k in keywords)]

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
        print_error(f"[proc] Failed: {e}")
