from diag_shell.output import print_error, print_warn
from diag_shell.utils.args import parse_args
import subprocess
import json


def disk(interpreter, args):
    """
    Display disk usage from `df -h --total`.

    Options:
      --grep <pattern>  Filter lines containing keyword
      --json            Output in JSON format
    """
    try:
        parsed = parse_args(args, flags={"--json"}, options={"--grep"})
        grep = parsed.get("--grep")
        json_mode = parsed.get("--json", False)

        result = subprocess.run(
            ["df", "-h", "--total"], capture_output=True, text=True, env={**interpreter.env, "LANG": "C"}
        )

        lines = result.stdout.strip().splitlines()
        header, *data = lines
        header = header.replace("Mounted on", "Mounted_on")
        cols = header.split()

        if grep:
            data = [line for line in data if grep in line]

        if json_mode:
            structured = []
            for line in data:
                parts = line.split(None, len(cols) - 1)
                if len(parts) == len(cols):
                    item = dict(zip(cols, parts))
                    if "Mounted_on" in item:
                        item["Mounted on"] = item.pop("Mounted_on")
                    structured.append(item)
            print(json.dumps(structured, indent=2))
        else:
            print("== Disk Usage ==")
            widths = [len(col) for col in cols]
            rows = []
            for line in data:
                parts = line.split(None, len(cols) - 1)
                if len(parts) == len(cols):
                    for i, part in enumerate(parts):
                        widths[i] = max(widths[i], len(part))
                    rows.append(parts)

            def format_row(row):
                return " | ".join(part.ljust(widths[i]) for i, part in enumerate(row))

            print(format_row([col.replace("Mounted_on", "Mounted on") for col in cols]))
            print("-+-".join("-" * w for w in widths))
            for row in rows:
                print(format_row(row))

        if result.returncode != 0:
            for line in result.stderr.strip().splitlines():
                print_warn(f"[WARN] {line}")
            print_warn(f"[WARN] Partial failure (exit code {result.returncode})")

    except Exception as e:
        print_error(f"[disk] Failed: {e}")
