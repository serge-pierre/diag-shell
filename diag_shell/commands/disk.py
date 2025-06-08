from diag_shell.output import print_table, print_warning, print_error
import subprocess


def disk(interpreter, args):
    """Display disk usage."""
    try:
        result = subprocess.run(
            ["df", "-h", "--total"],
            capture_output=True,
            text=True,
            env=interpreter.env
        )
        if result.stdout:
            lines = result.stdout.strip().splitlines()
            headers = lines[0].split()
            rows = [line.split(None, len(headers) - 1) for line in lines[1:]]
            print_table(headers, rows, title="Disk Usage")
        if result.stderr:
            print_warning(result.stderr.strip())
        if result.returncode != 0:
            print_warning(f"Partial failure (exit code {result.returncode})")
    except Exception as e:
        print_error(f"[disk] Failed: {e}")
