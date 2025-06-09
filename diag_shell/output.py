from typing import List, Dict
import shutil


def print_kv(data: Dict[str, str], title: str = None):
    """Display key-value pairs in aligned format."""
    if title:
        print(f"\n== {title} ==")
    width = max(len(k) for k in data)
    for key, value in data.items():
        print(f"{key.ljust(width)} : {value}")


def print_table(headers: List[str], rows: List[List[str]], title: str = None):
    """Display a formatted table."""
    if title:
        print(f"\n== {title} ==")
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(cell))

    # Print header
    header_line = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
    print(header_line)
    print("-+-".join("-" * w for w in col_widths))

    # Print rows
    for row in rows:
        print(" | ".join(cell.ljust(col_widths[i]) for i, cell in enumerate(row)))


def print_warning(message: str):
    print(f"[WARN] {message}")


def print_info(message: str):
    print(f"[INFO] {message}")


def print_error(message: str):
    print(f"[ERROR] {message}")


def print_error(message):
    print(f"\033[91m{message}\033[0m")


def print_warn(message):
    print(f"\033[93m{message}\033[0m")
