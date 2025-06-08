def parse_args(args, *, flags=None, options=None, strict=True):
    """
    Parse CLI-style arguments into a dict.

    - flags: set of options like '--json' that are boolean
    - options: set of options like '--grep' or '--limit' that expect a value
    - strict: if True, unknown options raise ValueError

    Returns:
        dict: {
            'args': [...],        # positional args
            '--json': True,      # flags present
            '--grep': 'PATH',    # options with value
        }
    """
    flags = flags or set()
    options = options or set()
    parsed = {"args": []}
    it = iter(args)

    for arg in it:
        if arg in flags:
            parsed[arg] = True
        elif arg in options:
            try:
                value = next(it)
                parsed[arg] = value
            except StopIteration:
                raise ValueError(f"Missing value for option {arg}")
        elif arg.startswith("--") and strict:
            raise ValueError(f"Unknown option: {arg}")
        else:
            parsed["args"].append(arg)

    return parsed
