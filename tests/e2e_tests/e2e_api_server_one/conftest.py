import threading
import time

import pytest

from api_compose.servers.api_server_one.app import build_api_server_one


@pytest.fixture(scope='session')
def rest_port():
    return 8085


@pytest.fixture
def start_api_server_one(rest_port):
    app = build_api_server_one(rest_port)
    thread = threading.Thread(target=app.run)
    thread.daemon = True
    thread.start()
    time.sleep(1)
    yield app.app
    thread.join(1)
