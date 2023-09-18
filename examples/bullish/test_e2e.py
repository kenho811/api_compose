"""
Script which simulates using the CLI
"""

import pytest
from _pytest.capture import CaptureFixture
from typer.testing import CliRunner

from api_compose.cli.main import app

runner = CliRunner()


@pytest.mark.authenticated
def test_run_bullish_action(capsys: CaptureFixture):
    """
    Simulates what happens when one runs

    acp manifest run actions/login_v2.yaml --ctx some_key=some_val
    """
    with capsys.disabled() as disabled:
        result = runner.invoke(app, ["run", "-e", "uat",
                                     "-f", "./manifests/actions/login_v2.yaml",
                                     "--ctx", "some_key=some_val"
                                     ])
        assert result.exit_code == 0, "Result is non-zero"


@pytest.mark.authenticated
def test_run_bullish_specification(capsys: CaptureFixture):
    """
    Simulates what happens when one runs only specification models
    """
    with capsys.disabled() as disabled:
        result = runner.invoke(app, [
            "run",
            "-e", "uat"
            "-m", "SpecificationModel"])
        assert result.exit_code == 0, "Result is non-zero"


@pytest.mark.authenticated
def test_run_bullish_can_cancel_all_specification(capsys: CaptureFixture):
    """
    Simulates what happens when one runs

    acp manifest run actions/login_v2.yaml --ctx some_key=some_val
    """
    with capsys.disabled() as disabled:
        result = runner.invoke(app, [
            "run",
            "-e", "uat",
            "-f", "./manifests/specifications/can_cancel_all_orders.yaml"
        ])
        assert result.exit_code == 0, "Result is non-zero"


@pytest.mark.authenticated
def test_run_bullish_exclude_tests(capsys: CaptureFixture):
    """
    Simulates what happens when one runs

    acp run
    """
    with capsys.disabled() as disabled:
        result = runner.invoke(app, [
            "run",
            "-e", "uat",
            "-T", "tests"
        ])
        assert result.exit_code == 0, "Result is non-zero"


def test_clean(capsys: CaptureFixture):
    """
    acp clean
    """
    with capsys.disabled() as disabled:
        result = runner.invoke(app, ["clean"])
        assert result.exit_code == 0, "Result is non-zero"
