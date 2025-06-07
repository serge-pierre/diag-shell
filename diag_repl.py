import sys
from replkit import repl
from diag_shell.diag_interpreter import DiagSystemInterpreter


def main():
    repl(
        interpreter=DiagSystemInterpreter(),
        argv=[
            "--prompt", "diag> ",
            "--hello", "Welcome to DiagShell!",
        ]
    )


if __name__ == "__main__":
    sys.exit(main())
