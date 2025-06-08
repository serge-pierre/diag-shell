from diag_shell.output import print_kv, print_error
import subprocess


def cpu(interpreter, args):
    """Display CPU load (1, 5, 15 min averages)."""
    try:
        output = subprocess.check_output(["uptime"], text=True, env=interpreter.env).strip()
        if "load average" in output:
            raw = output.split("load average:")[-1]
            parts = [s.strip().replace(",", ".") for s in raw.split(",")]
            values = [f"{float(p):.2f}" for p in parts[:3]]
            print_kv({
                "Last 1 min": values[0],
                "Last 5 min": values[1],
                "Last 15 min": values[2],
            }, title="CPU Load")
        else:
            print(output)
    except Exception as e:
        print_error(f"[cpu] Failed: {e}")
