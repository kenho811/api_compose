import pytest

from api_compose import FunctionsRegistry
from api_compose.services.common.jinja import get_jinja_functions, JinjaFunctionNamespaceClashException


def test_can_raise_jinja_function_namespace_clash_error(bad_jinja_namespace):
    with pytest.raises(JinjaFunctionNamespaceClashException):
        get_jinja_functions()


@pytest.fixture()
def bad_jinja_namespace():
    backup = [model.model_copy() for model in FunctionsRegistry.registry]

    FunctionsRegistry.registry = []

    @FunctionsRegistry.set(name='custom.some_func')
    def some_func():
        return 1

    @FunctionsRegistry.set(name='custom')
    def some_other_func():
        return 2

    yield

    # reset to original
    FunctionsRegistry.registry = backup
