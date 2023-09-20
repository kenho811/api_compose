import logging
import os

import pytest

# When running pytest, make logging level to debug
os.environ['LOGGING__LOGGING_LEVEL'] = str(logging.DEBUG)

import threading
import time

import connexion
from connexion.resolver import MethodViewResolver



############################################################
# Rest Action Fixtures


@pytest.fixture(scope='session')
def rest_port() -> int:
    return 8090


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
