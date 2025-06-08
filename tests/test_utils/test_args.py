import pytest
from diag_shell.utils.args import parse_args


def test_parse_flags():
    args = ["--json", "foo"]
    out = parse_args(args, flags={"--json"})
    assert out["--json"] is True
    assert out["args"] == ["foo"]


def test_parse_options():
    args = ["--grep", "PATH", "foo"]
    out = parse_args(args, options={"--grep"})
    assert out["--grep"] == "PATH"
    assert out["args"] == ["foo"]


def test_parse_mixed():
    args = ["--json", "--grep", "SSH", "val"]
    out = parse_args(args, flags={"--json"}, options={"--grep"})
    assert out["--json"] is True
    assert out["--grep"] == "SSH"
    assert out["args"] == ["val"]


def test_parse_missing_option_value():
    with pytest.raises(ValueError):
        parse_args(["--grep"], options={"--grep"})


def test_parse_unknown_option_strict():
    with pytest.raises(ValueError, match="Unknown option: --jso"):
        parse_args(["--jso"], flags={"--json"}, options={"--grep"})
