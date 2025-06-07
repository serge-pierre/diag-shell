# DiagShell

DiagShell is a pluggable system diagnostics interpreter based on [replkit](https://github.com/serge-pierre/replkit).

It provides simple CLI commands for inspecting CPU, memory, disk, network, and uptime information using existing system tools.

## Installation

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
