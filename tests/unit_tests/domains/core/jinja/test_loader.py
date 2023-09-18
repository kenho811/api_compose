import pytest


@pytest.mark.parametrize('template_str',
                         [
                             ('{{ some_macro(12) }}'),
                             ('{{ some_macro(val) }}'),
                         ]
                         )
def test_template_str_cannot_load_macro(template_str, test_action_jinja_context, test_run_time_jinja_engine):
    # Act
    str_, is_success, exec = test_run_time_jinja_engine.set_template_by_string(template_str).render_to_str(test_action_jinja_context)
    # Assert
    assert not is_success


