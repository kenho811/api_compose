import pytest

from api_compose.core.utils.exceptions import NoMatchesFoundWithFilter


def test_self_refers_to_current_action(
        test_action_jinja_context,
        test_run_time_jinja_engine,
):
    str_, is_success, exec = test_run_time_jinja_engine.set_template_by_string(
        "{{ action('get_image') | output_body == action('self')| output_body }}"
    ).render_to_str(test_action_jinja_context)

    assert str_.strip().lower() == 'true', 'ERROR - self is NOT referring to get_image action !!!'


@pytest.mark.parametrize(
    'template',
    [
        # config headers
        ("{{ action('get_image')| acp.actions.config_headers == {'token': 'Bearer 1234'} }}"),
        ("{{ action('get_image')| config_headers == {'token': 'Bearer 1234'} }}"),

        # config method
        ("{{ action('get_image')| acp.actions.config_method == 'GET' }}"),
        ("{{ action('get_image')| config_method == 'GET' }}"),

        # config params
        ("{{ action('get_image')| acp.actions.config_params == {'query': 'dog'} }}"),
        ("{{ action('get_image')| config_params == {'query': 'dog'} }}"),

        # config body
        ("{{ action('get_image')| acp.actions.config_body == {'size': 12} }}"),
        ("{{ action('get_image')| config_body == {'size': 12} }}"),

        # input url
        ("{{ action('get_image')| acp.actions.input_url == 'http://abc.com/v1/images' }}"),
        ("{{ action('get_image')| input_url == 'http://abc.com/v1/images' }}"),

        # input body
        ("{{ action('get_image')| acp.actions.input_body| jpath('$.size') == 12 }}"),
        ("{{ action('get_image')| input_body| jpath('$') == {'size': 12} }}"),

        # output body
        ("{{ action('get_image')| acp.actions.output_body| jpath('$.field_one') == 1234 }}"),
        ("{{ action('get_image')| output_body| jpath('$.val') == 12 }}"),

        # output headers
        ("{{ action('get_image')| acp.actions.output_headers| jpath('$.Server') == 'Google Frontend' }}"),
        ("{{ action('get_image')| output_headers| jpath('$.Server') == 'Google Frontend' }}"),

        # output status code
        ("{{ action('get_image')| acp.actions.output_status_code == 200 }}"),
        ("{{ action('get_image')| output_status_code == 200 }}"),
    ]
)
def test_can_filter_action_with_success(
        test_action_jinja_context,
        test_run_time_jinja_engine,
        template,
):
    str_, is_success, exec = test_run_time_jinja_engine.set_template_by_string(
        template
    ).render_to_str(test_action_jinja_context)

    assert str_.strip().lower() == 'true', str_


def test_can_pass_filter_into_global(
        test_action_jinja_context,
        test_run_time_jinja_engine,
):
    str_, is_success, exec = test_run_time_jinja_engine.set_template_by_string(
        """{{ repeat(action('get_image')| acp.actions.config_method ) == 'GETGET' }}""",
    ).render_to_str(test_action_jinja_context)

    assert str_.strip().lower() == 'true', str_


def test_when_action_not_exist__can_raise_no_matches_found_error(
        test_action_jinja_context,
        test_run_time_jinja_engine,
):
    str_, is_success, exec = test_run_time_jinja_engine.set_template_by_string(
        """{{ action('does_not_exist') }}}"""
    ).render_to_str(test_action_jinja_context)

    assert type(exec) == NoMatchesFoundWithFilter
