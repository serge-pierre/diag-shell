# Makefile for DiagShell project
PYTHON ?= python
PIP ?= $(PYTHON) -m pip

.PHONY: install lint format test clean help

install:
	$(PIP) install --upgrade pip setuptools
	$(PIP) install -e .[dev]

lint:
	$(PYTHON) -m ruff check diag_shell tests

format:
	$(PYTHON) -m black diag_shell tests

test:
	$(PYTHON) -m pytest -v

clean:
	find . -type d -name "**pycache**" -exec rm -r {} +
	rm -rf .pytest_cache .mypy_cache .ruff_cache dist build *.egg-info

help:
	@echo "Available targets:"
	@echo "  install  - Install project + dev deps"
	@echo "  lint     - Run linter (ruff)"
	@echo "  format   - Format code (black)"
	@echo "  test     - Run tests with pytest"
	@echo "  clean    - Remove caches and build artifacts"
	@echo "  help     - Show this message"
