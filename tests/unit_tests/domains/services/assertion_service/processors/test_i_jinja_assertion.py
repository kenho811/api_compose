import pytest

from api_compose.services.assertion_service.processors.i_jinja_assertion import InteractiveJinjaAssertion


# @pytest.mark.skip
@pytest.mark.parametrize(
    'command',
    [
        ("""
        render "{{ action('login') | output_headers| jpath('$.Server') != action('get_image') | output_headers| jpath('$.Server') }}"
        """),

        ("""
        render "{{ action('login') | output_status_code == action('get_image') | output_status_code }}"
        """),

    ]
)
def test_can_interactively_assert_with_jinja_template(
        test_run_time_jinja_engine,
        test_action_jinja_context,
        command,
):
    # Setup
    processor = InteractiveJinjaAssertion(
        jinja_context=test_action_jinja_context,
        jinja_engine=test_run_time_jinja_engine,
    )

    processor.onecmd(command)

    for assertion in processor.assertions:
        assert assertion.is_success, assertion
