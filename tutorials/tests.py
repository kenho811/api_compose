"""
Pytest to test tutorials
"""
import os

from _pytest.capture import CaptureFixture
from typer.testing import CliRunner

from api_compose.cli.main import app

runner = CliRunner()

import pytest
import subprocess


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    subprocess.call(['/start_server.sh'])


def test_lesson_one(capsys: CaptureFixture):
    """
    Simulates what happens when one runs

    acp manifest run actions/login_v2.yaml --ctx some_key=some_val
    """
    os.chdir('lesson_one__setup')

    try:
        with capsys.disabled() as disabled:
            result = runner.invoke(
                app,
                ["run",
                 "-f", "./get_pets.yaml",
                 "--ctx", "some_key=some_val"
                 ])
            assert result.exit_code == 0, "Result is non-zero"
    finally:
        os.chdir('../')

