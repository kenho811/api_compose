import pytest
from typer.testing import CliRunner


@pytest.fixture()
def test_runner() -> CliRunner:
    return CliRunner()
