from diag_shell.output import print_error
import subprocess


def crontab(interpreter, args):
    """Display the current user's crontab entries."""
    try:
        output = subprocess.check_output(
            ["crontab", "-l"], text=True, env=interpreter.env
        ).strip()
        print(output)
    except subprocess.CalledProcessError as e:
        if e.returncode == 1:
            print("(no crontab for user)")
        else:
            print_error(f"[crontab] Failed: {e}")
    except Exception as e:
        print_error(f"[crontab] Failed: {e}")
