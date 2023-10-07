from _pytest.capture import CaptureFixture
from typer.testing import CliRunner

from api_compose import GlobalSettingsModelSingleton
from api_compose.cli.main import app
from api_compose.root.models.session import parse_session_from_yaml_file

runner = CliRunner()


def test_can_update_pet(
        capsys: CaptureFixture,
        start_api_server_one
):
    with capsys.disabled() as disabled:
        GlobalSettingsModelSingleton.set() # reset settings

        result = runner.invoke(
            app,
            [
                "run",
                "-f",
                "./manifests/specifications/can_update_pet_by_id.yaml",
                "--id",
                "api_server_one__specification__can_update_pet",
            ],
            standalone_mode=False,
            catch_exceptions=False,
        )

        session = parse_session_from_yaml_file(result.return_value[0])
        is_success = result.return_value[1]

        assert len(session.specifications) == 1
        assert len(session.specifications[0].scenarios) == 1
        assert len(session.specifications[0].scenarios[0].actions) == 3
        assert is_success
