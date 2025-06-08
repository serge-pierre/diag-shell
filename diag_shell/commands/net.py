from diag_shell.output import print_error
import subprocess


def net(interpreter, args):
    """Display network interfaces."""
    try:
        output = subprocess.check_output(["ip", "-brief", "addr"], text=True, env=interpreter.env).strip()
        print(output)
    except Exception as e:
        print_error(f"[net] Failed: {e}")
