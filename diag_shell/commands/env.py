from diag_shell.output import print_error
import subprocess


def env(interpreter, args):
    """Display environment variables."""
    try:
        output = subprocess.check_output(
            ["env"], text=True, env=interpreter.env
        ).strip()
        print(output)
    except Exception as e:
        print_error(f"[env] Failed: {e}")
