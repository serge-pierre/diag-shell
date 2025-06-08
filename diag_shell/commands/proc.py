from diag_shell.output import print_error
import subprocess


def proc(interpreter, args):
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
        output = subprocess.check_output(["ps", "aux"], text=True, env=interpreter.env).splitlines()
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
