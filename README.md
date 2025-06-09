![Python](https://img.shields.io/badge/python-3.8%2B-blue)
[![License](https://img.shields.io/github/license/serge-pierre/diag-shell)](./LICENSE)
[![GitHub release](https://img.shields.io/github/v/release/serge-pierre/diag-shell)](https://github.com/serge-pierre/diag-shell/releases)
![Tested with pytest](https://img.shields.io/badge/tested%20with-pytest-1f425f.svg)

# DiagShell

**DiagShell** is a command-line REPL for exploring live system diagnostics.
It is based on [`replkit`](https://github.com/serge-pierre/replkit), a flexible CLI interpreter framework.

---

## Getting Started

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

## Philosophy

DiagShell is designed for **clarity**, **utility**, and **modularity**:

- One-line commands to inspect live system state
- Simple composable options (`--grep`, `--json`, etc.)
- Easily extendable with your own commands

---

## Features

### Interactive REPL

- Tab completion
- Persistent history
- Extensible interpreter interface

### System Diagnostic Commands

| Command   | Description                               |
| --------- | ----------------------------------------- |
| `cpu`     | Load average (1/5/15 min)                 |
| `mem`     | RAM + Swap usage                          |
| `disk`    | Disk usage from `df -h`                   |
| `net`     | Network interfaces & addresses            |
| `uptime`  | System uptime summary                     |
| `proc`    | Live processes with keyword filtering     |
| `env`     | Environment variables                     |
| `who`     | Logged-in users                           |
| `top`     | Top CPU consumers (`ps aux --sort=-%cpu`) |
| `crontab` | Current user crontab entries              |

### Options by Command

| Option    | `proc` | `top` | `disk` | `who` | `env` | `crontab` |
| --------- | ------ | ----- | ------ | ----- | ----- | --------- |
| `--grep`  | ✅     | ✅    | ✅     | ✅    | ✅    | ✅        |
| `--json`  | ✅     | ✅    | ✅     | ✅    | ✅    | ✅        |
| `--limit` | ✅     | ✅    | ❌     | ❌    | ❌    | ❌        |
| `--or`    | ✅     | ❌    | ❌     | ❌    | ❌    | ❌        |

_Options combinables entre elles (ex: `proc ssh --limit 5 --json`)_

---

## Testing

```bash
make test
```

Couvre tous les modules et options via `pytest`

---

## Developing

```bash
make format     # Format with black
make lint       # Lint with flake8
make install    # Dev install with editable mode
```

Pour ajouter une commande :

- Créer un fichier `diag_shell/commands/<name>.py`
- Ajouter une fonction `<name>(interpreter, args)`
- Enregistrer-la dans `commands/__init__.py`

---

## Versioning

- `v0.1.0` : MVP REPL + commandes de base CPU/MEM/NET
- `v0.2.0` : Architecture modulaire + tests par commande
- `v0.3.0` : Ajout commandes système (who, env, ports...)
- `v0.3.1` : Options enrichies : `--grep`, `--json`, `--limit`, `--or`

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
