from diag_shell.output import print_error
import subprocess


def who(interpreter, args):
    """Display users currently logged in."""
    try:
        output = subprocess.check_output(
            ["who"], text=True, env=interpreter.env
        ).strip()
        if output:
            print(output)
        else:
            print("No users currently logged in.")
    except Exception as e:
        print_error(f"[who] Failed: {e}")
