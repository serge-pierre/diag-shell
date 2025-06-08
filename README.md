![Python](https://img.shields.io/badge/python-3.8%2B-blue)
[![License](https://img.shields.io/github/license/serge-pierre/replkit)](./LICENSE)

# DiagShell

DiagShell is a pluggable system diagnostics interpreter based on [replkit](https://github.com/serge-pierre/replkit).

It provides simple CLI commands for inspecting CPU, memory, disk, network, and uptime information using existing system tools.

## Features

- Modular REPL interpreter based on replkit
- Diagnostics commands: `cpu`, `mem`, `disk`, `net`, `uptime`, `proc`
- Formatted and readable output (`print_kv`, `print_table`)
- Locale-independent parsing (`LANG=C`)
- Filterable `proc` with support for `--or`
- Persistent aliases and history
- Tested with pytest (100% success)

## Version History

### v0.2.0 (2025-06-07)

- First fully stable release with formatted diagnostics output
- Forced locale (`LANG=C`) for universal parsing
- `print_table()` for aligned views of disk and memory
- `proc` supports `AND` and `--or` filtering
- Unit tests pass (10/10)

### Installation

```bash
git clone https://github.com/serge-pierre/diag-shell.git
cd diag-shell
python -m venv venv
source venv/bin/activate
```

### Environnement initialisation

```bash
pip install --upgrade pip setuptools
pip install -e .
```

Or more simple

```
make install
```

See Makefile and try make help to see what is possible.

### Run DiagShell

```bash
python diag_repl.py
```

---

## Contributing

PRs and bug reports are welcome! Please add tests for any new feature or bugfix.

---

## License

MIT

© 2025–present Serge Pierre

---

## Author

Serge Pierre  
[https://github.com/serge-pierre](https://github.com/serge-pierre)
