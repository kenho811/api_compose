import yaml
from _pytest.capture import CaptureFixture
from typer.testing import CliRunner

from api_compose.cli.main import app
from api_compose.root import SessionModel

runner = CliRunner()


def parse_session_file(session_yaml_path: str) -> SessionModel:
    with open(session_yaml_path, 'r') as f:
        dict_ = yaml.load(f, Loader=yaml.FullLoader)
        return SessionModel(**dict_)


def test_can_create_pet(capsys: CaptureFixture, start_api_server_one):
    with capsys.disabled() as disabled:
        result = runner.invoke(
            app,
            [
                "run",
                "-f",
                "./manifests/actions/create_pet.yaml",
                "--id",
                "action__can_create_pet",
            ],
            standalone_mode=False,
        )
        assert result.exit_code == 0, "Result is non-zero"
        session = parse_session_file(result.return_value)

        print(session)
