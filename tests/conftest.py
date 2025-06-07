import pytest

# Shared fixtures or hooks can go here
# Example: default interpreter instance for reuse

import diag_shell.diag_interpreter as diag_mod


@pytest.fixture
def diag():
    return diag_mod.DiagSystemInterpreter()
