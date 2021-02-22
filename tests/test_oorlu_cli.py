#!/usr/bin/env python

"""Tests for `oorlu_cli` package."""
from contextlib import nullcontext

import pytest
import requests
from click.testing import CliRunner

from oorlu_cli import cli
from oorlu_cli.validator import ValidationError, validate_long_url


@pytest.mark.parametrize(
    "long_url, fail_expected",
    [
        ("www.google.com", False),
        ("google", True),
        ("wrongurl.", True),
        ("https://", True),
        ("https://test.com", False),
        ("https://google.com", False),
        ("www.google.com", False),
    ],
)
def test_validate_long_url(long_url, fail_expected):
    with pytest.raises(ValidationError) if fail_expected else nullcontext():
        validate_long_url(long_url)


def test_command_line_interface(monkeypatch):
    """Test the CLI."""
    runner = CliRunner()
    help_text = "Show this message and exit"
    no_argument_result = runner.invoke(cli.main)
    assert no_argument_result.exit_code == 0
    assert help_text in no_argument_result.output

    help_result = runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0
    assert help_text in help_result.output

    wrong_url_result = runner.invoke(cli.main, ["google"])
    assert wrong_url_result.exit_code == 2
    assert "Invalid value for LONG_URL" in wrong_url_result.output

    wrong_limit_result = runner.invoke(cli.main, ["google.com", "-l", "-1"])
    assert wrong_limit_result.exit_code == 2
    assert "Invalid value for limit" in wrong_limit_result.output

    def mock_res_error(*args, **kwargs):
        raise requests.exceptions.RequestException

    monkeypatch.setattr("requests.post", mock_res_error)
    connection_error_result = runner.invoke(cli.main, ["test.com"])
    assert connection_error_result.exit_code == 1
    assert "API / Connection error - please see if https://oor.lu works" in connection_error_result.output
