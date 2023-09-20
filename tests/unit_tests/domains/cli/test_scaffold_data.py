import contextlib
import os
from pathlib import Path

from _pytest.capture import CaptureFixture

from api_compose.cli import main
from api_compose.cli.main import app


@contextlib.contextmanager
def working_directory(target_path):
    """Changes working directory and returns to previous on exit."""
    prev_cwd = Path.cwd()
    os.chdir(target_path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)


def test_scaffold_data_can_compile(
        capsys: CaptureFixture,
        test_runner,
):
    target_path = Path(main.__file__).parent.joinpath('scaffold_data')
    with working_directory(target_path=target_path):
        print(Path.cwd())
        with capsys.disabled() as disabled:
            result = test_runner.invoke(app, [
                "compile",
            ]
                                        )
            assert result.exit_code == 0, "Result is non-zero"
