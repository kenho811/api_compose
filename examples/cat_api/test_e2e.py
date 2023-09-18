"""
Script


"""
import pytest
from _pytest.capture import CaptureFixture
from typer.testing import CliRunner

from api_compose.cli.main import app

runner = CliRunner()


@pytest.mark.unauthenticated
def test_compile_action(capsys: CaptureFixture):
    with capsys.disabled() as disabled:
        result = runner.invoke(app, ["compile", "-f", "actions/get_image.yaml", "-F", "actions/get_categories.yaml"])
        assert result.exit_code == 0, "Result is non-zero"


@pytest.mark.authenticated
def test_run_action(capsys: CaptureFixture):
    with capsys.disabled() as disabled:
        result = runner.invoke(app, ["run", "-f", "actions/get_image.yaml", "--ctx", "some_key=some_val"])
        assert result.exit_code == 0, "Result is non-zero"


@pytest.mark.authenticated
def test_run_scenario_group(capsys: CaptureFixture):
    with capsys.disabled() as disabled:
        result = runner.invoke(app, ["run", "-f", "specifications/can_vote_image.yaml"])
        assert result.exit_code == 0, "Result is non-zero"


@pytest.mark.authenticated
def test_run(capsys: CaptureFixture):
    with capsys.disabled() as disabled:
        result = runner.invoke(app, ["run", "--ctx", "abc=123"])
        assert result.exit_code == 0, "Result is non-zero"
