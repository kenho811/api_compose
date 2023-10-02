import requests
from _pytest.capture import CaptureFixture
from typer.testing import CliRunner

from api_compose.cli.main import app
from api_compose.root.models.session import parse_session_from_yaml_file

runner = CliRunner()


def test_can_create_pet(capsys: CaptureFixture, start_api_server_one):
    with capsys.disabled() as disabled:
        result = runner.invoke(
            app,
            [
                "run",
                "-f",
                "./manifests/actions/create_pet.yaml",
                "-e",
                "base",
                "--id",
                "action__create_pet",
            ],
            standalone_mode=False,
        )
        session = parse_session_from_yaml_file(result.return_value)

        assert len(session.specifications) == 1
        assert len(session.specifications[0].scenarios) == 1
        assert len(session.specifications[0].scenarios[0].actions) == 1
        assert session.specifications[0].scenarios[0].actions[0].output.status_code == 201