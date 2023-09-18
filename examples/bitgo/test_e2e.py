"""
Script


"""
import pytest
from _pytest.capture import CaptureFixture
from typer.testing import CliRunner

from api_compose.cli.main import app

runner = CliRunner()


@pytest.mark.authenticated
def test_run(capsys: CaptureFixture):
    with capsys.disabled() as disabled:
        result = runner.invoke(app, ["run", "-m", "SpecificationModel"])
        assert result.exit_code == 0, "Result is non-zero"
