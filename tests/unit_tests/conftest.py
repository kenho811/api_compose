import logging
import os

from typer.testing import CliRunner

from api_compose import FunctionsRegistry, FunctionType
from api_compose.services.common.jinja import build_compile_time_jinja_engine, build_runtime_jinja_engine
from api_compose.services.composition_service.jinja.context import ActionJinjaContext
from api_compose.services.composition_service.models.actions.inputs.http_inputs import JsonHttpActionInputModel

# When running pytest, make logging level to debug
os.environ['LOGGING__LOGGING_LEVEL'] = str(logging.DEBUG)

import threading
import time
from pathlib import Path

import connexion
from connexion.resolver import MethodViewResolver

from api_compose.core.jinja.core.engine import JinjaEngine
from api_compose.services.composition_service.models.actions.outputs.http_outputs import JsonHttpActionOutputModel
from tests.unit_tests.fixtures import *  # noqa. Import pytest fixtures


@FunctionsRegistry.set(
    name='test.repeat',
    func_type=FunctionType.JinjaGlobal,
    alias=['repeat']
)
def repeat_string(some_string: str, times: int = 2) -> str:
    return some_string * times


@pytest.fixture(scope='session')
def test_jinja_function():
    # can only register once
    @FunctionsRegistry.set(name='get_one', func_type=FunctionType.JinjaGlobal)
    def get_one():
        return 1


@pytest.fixture()
def test_run_time_jinja_engine(
        test_jinja_function,
) -> JinjaEngine:
    return build_runtime_jinja_engine()


@pytest.fixture()
def test_compile_time_jinja_engine(
        test_jinja_function,
        test_manifests_search_path,
) -> JinjaEngine:
    return build_compile_time_jinja_engine(
        test_manifests_search_path
    )


@pytest.fixture
def test_action_jinja_context() -> ActionJinjaContext:
    previous_action_model = JsonHttpActionModel(model_name='JsonHttpActionModel',
        id='login',
        execution_id='login',
        input=JsonHttpActionInputModel(
            url='http://abc.com/v1/login',
            params={},
            method='POST',
        ),
        output=JsonHttpActionOutputModel(
            headers={
                'Server': 'cloudflare',
                'Transfer-Encoding': 'chunked',
                'Vary': 'Accept-Encoding',
                'X-Frame-Options': 'SAMEORIGIN',
            },
            body={
                'token': 1234,
                'is_true': True,
                'float': 1.23,
                'animal': 'dog',
            },
            status_code=200,
        ),
    )

    current_action_model = JsonHttpActionModel(model_name='JsonHttpActionModel',
        id='get_image',
        execution_id='get_image',
        config=JsonHttpActionConfigModel(
            url=StringTemplatedTextField(
                template='http://abc.com/v1/images'
            ),
            headers=JsonTemplatedTextField(
                template=json.dumps({
                    'token': "Bearer {{ action('login')| output_body | jpath('$.token') }}"
                }),
            ),
            params=JsonTemplatedTextField(
                template=json.dumps(
                    {'query': "{{ action('login') | output_body | jpath('$.animal') }}"}
                )
            ),
            method=StringTemplatedTextField(
                template='GET'
            ),
            body=JsonTemplatedTextField(
                template=json.dumps(
                    {'size': 12}
                )
            )
        ),
        input=JsonHttpActionInputModel(
            url='http://abc.com/v1/images',
            headers={'token': 'Bearer 1234'},
            params={
                'query': 'dogs',
            },
            method='GET',
            body={'size': 12},
        ),
        output=JsonHttpActionOutputModel(
            body={
                'field_one': 1234,
                'val': 12,
            },
            headers={
                'Content-Length': '101',
                'Date': 'Sat, 26 Aug 2023 15:05:39 GMT',
                'Server': 'Google Frontend',
            },
            status_code=200,
        ),
    )
    action_models = [previous_action_model, current_action_model]
    return ActionJinjaContext(
        action_models=action_models,
        current_action_model=current_action_model
    )


@pytest.fixture()
def test_manifests_search_path() -> Path:
    return Path(__file__).parent.joinpath('resources/manifests').absolute()


@pytest.fixture()
def test_runner() -> CliRunner:
    return CliRunner()


############################################################
# Rest Action Fixtures


@pytest.fixture(scope='session')
def rest_port() -> int:
    return 8085


@pytest.fixture(scope='session')
def rest_base_url(rest_port) -> str:
    return f"http://localhost:{rest_port}"


@pytest.fixture(scope='session')
def rest_server(rest_port):
    app = build_rest_server(rest_port)
    thread = threading.Thread(target=app.run)
    thread.daemon = True
    thread.start()
    logging.info('Spinning up flask server...')
    time.sleep(1)
    yield app.app
    thread.join(1)


def build_rest_server(rest_port):
    app = connexion.App(__name__,
                        specification_dir='resources',
                        port=rest_port,
                        host='localhost'
                        )
    app.add_api('http_openapi.yaml', resolver=MethodViewResolver('views'))
    return app


if __name__ == '__main__':
    # Running Swagger in standalone mode for debugging
    import sys

    port = 8085
    url = f'http://localhost:{port}/ui'
    print(f"Please visit the UI at {url=}")
    sys.path.append('resources')
    app = build_rest_server(8085)
    app.run()
