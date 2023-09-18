import pytest
from jinja2 import UndefinedError

from api_compose.core.utils.exceptions import NoMatchesFoundWithFilter


@pytest.mark.parametrize(
    'template_str, expected',
    [
        ("Bearer {{ action('login') | output_body| jpath('$.token') }}",
         ("Bearer 1234", True, None)
         ),
    ]
)
def test_successful_rendering_returns_rendered_string(
        template_str,
        expected,
        test_action_jinja_context,
        test_run_time_jinja_engine):
    actual = test_run_time_jinja_engine.set_template_by_string(template_str).render_to_str(
        test_action_jinja_context)
    assert actual == expected


@pytest.mark.parametrize(
    'template_str, expected_str,expected_is_success,expected_exec',
    [
        # Non-existent Global
        ("""Key:{{ does_not_exist() }}""",
         """Key:{{ does_not_exist() }}""",
          False,
          UndefinedError,
         ),

        # Non-existent Action
        ("""Key:{{ action('non_existent_execution_id') | output_body }}""",
         """Key:{{ action('non_existent_execution_id') | output_body }}""",
          False,
          NoMatchesFoundWithFilter,
         ),
    ]
)
def test_unsuccessful_rendering_returns_error(
        template_str,
        test_action_jinja_context,
        expected_str,
        expected_is_success,
        expected_exec,
        test_run_time_jinja_engine
):
    actual_str, actual_is_success, exec = test_run_time_jinja_engine.set_template_by_string(
        template_str).render_to_str(test_action_jinja_context)

    assert actual_str == expected_str
    assert actual_is_success == expected_is_success
    assert type(exec) == expected_exec
