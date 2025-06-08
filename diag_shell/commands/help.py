from diag_shell.output import print_error


def help(interpreter, args):
    """
    List available commands, or show help for a specific command.

    Usage:
      help              List all commands
      help <command>    Show help for a specific command
    """
    if not args:
        print("Available commands:")
        for cmd in sorted(interpreter.commands):
            doc = interpreter.commands[cmd].__doc__ or ""
            first = doc.strip().split("\n")[0]
            print(f"  {cmd:<10} - {first.strip()}")
    else:
        for cmd in args:
            if cmd in interpreter.commands:
                print(f"Help for command '{cmd}':\n")
                print(interpreter.commands[cmd].__doc__ or "(No documentation)\n")
            else:
                print_error(f"Unknown command: {cmd}")
