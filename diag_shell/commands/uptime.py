from diag_shell.output import print_kv, print_error
import subprocess


def uptime(interpreter, args):
    """Display system uptime."""
    try:
        output = subprocess.check_output(
            ["uptime", "-p"], text=True, env=interpreter.env
        ).strip()
        print_kv({"Uptime": output}, title="System Uptime")
    except Exception as e:
        print_error(f"[uptime] Failed: {e}")
