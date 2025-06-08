from diag_shell.output import print_error
import subprocess


def ports(interpreter, args):
    """Display open listening ports (TCP/UDP)."""
    try:
        output = subprocess.check_output(
            ["ss", "-tuln"], text=True, env=interpreter.env
        ).strip()
        print(output)
    except Exception as e:
        print_error(f"[ports] Failed: {e}")
