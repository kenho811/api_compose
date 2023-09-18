import pytest


@pytest.mark.parametrize(
    'template',
    [
        # jpath
        ("{{ dict(field_one=12)| jpath('$.field_one') == 12 }}"),
        ("{{ dict(field_one=12)| acp.paths.jpath('$.field_one') == 12 }}"),

    ]
)
def test_can_filter_by_jpath(
        test_action_jinja_context,
        test_run_time_jinja_engine,
        template,
):
    str_, is_success, exec = test_run_time_jinja_engine.set_template_by_string(
        template
    ).render_to_str(test_action_jinja_context)

    assert str_.strip().lower() == 'true', str_
