import requests
from _pytest.capture import CaptureFixture
from typer.testing import CliRunner

from api_compose import GlobalSettingsModelSingleton
from api_compose.cli.main import app
from api_compose.root.models.session import parse_session_from_yaml_file

runner = CliRunner()


def test_can_read_pets(capsys: CaptureFixture, start_api_server_one):
    with capsys.disabled() as disabled:
        GlobalSettingsModelSingleton.set() # reset settings

        result = runner.invoke(
            app,
            [
                "run",
                "-f",
                "./manifests/actions/read_pets.yaml",
                "--id",
                "api_server_one__action__read_pet",
            ],
            standalone_mode=False,
            catch_exceptions=False, # Let exception bubble up
        )
        session = parse_session_from_yaml_file(result.return_value[0])
        is_success = result.return_value[1]

        assert len(session.specifications) == 1
        assert len(session.specifications[0].scenarios) == 1
        assert len(session.specifications[0].scenarios[0].actions) == 1
        assert session.specifications[0].scenarios[0].actions[0].output.status_code == 200
        assert is_success, result.exception


