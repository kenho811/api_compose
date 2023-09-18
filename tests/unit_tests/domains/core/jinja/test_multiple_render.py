import pytest

from api_compose.core.jinja.core.context import BaseJinjaContext
from api_compose.services.common.models.text_field.templated_text_field import YamlTemplatedTextField
from api_compose.services.common.models.text_field.text_field import TextFieldFormatEnum


@pytest.fixture
def multisyntax_template() -> str:
    return """
id: abc
[% for i in range(2) %]
execution_id_[[ i ]] : [[ compile_time_var ]]
[% endfor %]
headers: |
    { "content": "{{ run_time_var }}" }
"""


@pytest.fixture()
def test_jinja_context():
    return BaseJinjaContext(
        compile_time_var='from_compile_time!',
        run_time_var='from_run_time!',
    )


def test_multiple_render(
        multisyntax_template,
        test_run_time_jinja_engine,
        test_compile_time_jinja_engine,
        test_jinja_context):
    actual_one, is_success, exec = test_compile_time_jinja_engine.set_template_by_string(
        multisyntax_template).render_to_str(test_jinja_context)
    assert is_success

    templated_field = YamlTemplatedTextField(template=actual_one, format=TextFieldFormatEnum.YAML).render_to_text(
        test_run_time_jinja_engine, test_jinja_context).deserialise_to_obj()
    assert templated_field.obj == {
        'id': 'abc',
        'execution_id_0': 'from_compile_time!',
        'execution_id_1': 'from_compile_time!',
        'headers': '{ "content": "from_run_time!" }',
    }
