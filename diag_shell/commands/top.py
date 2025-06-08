from diag_shell.output import print_error
import subprocess


def top(interpreter, args):
    """Display top 5 CPU-consuming processes."""
    try:
        output = (
            subprocess.check_output(
                ["ps", "aux", "--sort=-%cpu"], text=True, env=interpreter.env
            )
            .strip()
            .splitlines()
        )
        top_output = output[:6] if len(output) >= 6 else output
        print("\n".join(top_output))
    except Exception as e:
        print_error(f"[top] Failed: {e}")
