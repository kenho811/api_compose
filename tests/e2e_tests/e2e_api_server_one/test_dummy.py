from _pytest.capture import CaptureFixture
from typer.testing import CliRunner

from api_compose.cli.main import app

runner = CliRunner()


def test_run(capsys: CaptureFixture, start_api_server_one):
    with capsys.disabled() as disabled:
        result = runner.invoke(app, ["run", "--ctx", "abc=123"])
        assert result.exit_code == 0, "Result is non-zero"
