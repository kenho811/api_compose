import pytest


@pytest.mark.parametrize(
    'template',
    [
        ("""{{ action('login')| output_body| jpath('$.float') | acp.utils.double_quote }} """),
        ("""{{ action('login')| output_body| jpath('$.float') | double_quote }} """),
    ]
)
def test_can_double_quote(
        test_action_jinja_context,
        test_run_time_jinja_engine,
        template,
):
    str_, is_success, exec = test_run_time_jinja_engine.set_template_by_string(
        template
    ).render_to_str(test_action_jinja_context)

    assert str_.strip().lower() == '"1.23"'


@pytest.mark.parametrize(
    'template',
    [
        ("""{{ action('login')| output_body| jpath('$.float') | acp.utils.single_quote }} """),
        ("""{{ action('login')| output_body| jpath('$.float') | single_quote }} """),
    ]
)
def test_can_single_quote(
        test_action_jinja_context,
        test_run_time_jinja_engine,
        template
):
    str_, is_success, exec = test_run_time_jinja_engine.set_template_by_string(
        template
    ).render_to_str(test_action_jinja_context)

    assert str_.strip().lower() == "'1.23'"
