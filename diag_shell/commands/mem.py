from diag_shell.output import print_table, print_error
import subprocess


def mem(interpreter, args):
    """Display memory usage."""
    try:
        output = (
            subprocess.check_output(["free", "-h"], text=True, env=interpreter.env)
            .strip()
            .splitlines()
        )
        if len(output) < 2:
            raise ValueError("Unexpected output from 'free -h'")

        raw_headers = output[0].split()
        headers = ["Type"] + raw_headers
        data_lines = output[1:]
        rows = []

        for line in data_lines:
            parts = line.split()
            if not parts:
                continue
            label = parts[0].rstrip(":")
            values = parts[1:]
            values += ["-"] * (len(raw_headers) - len(values))
            rows.append([label] + values)

        print_table(headers, rows, title="Memory Usage")
    except Exception as e:
        print_error(f"[mem] Failed: {e}")
