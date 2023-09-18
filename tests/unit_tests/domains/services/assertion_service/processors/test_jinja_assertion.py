import pytest
from api_compose.services.assertion_service.models.jinja_assertion import JinjaAssertionModel, AssertionStateEnum

from api_compose.services.assertion_service.processors.jinja_assertion import JinjaAssertion



@pytest.mark.parametrize(
    'test_template, is_success',
    [
        ("{{ action('get_image') | output_body| jpath('$.val') is number }}", True),
        ("{{ action('get_image') | output_body| jpath('$.val') is undefined }}", False),
        ("{{ val == 11 }}", False),
        ("{{ not_exist == 12 }}", False),
    ]
)
def test_can_assert_with_jinja_template(
        test_run_time_jinja_engine,
        test_action_jinja_context,

        test_template,
        is_success,
):
    jinja_assertion_model = JinjaAssertionModel(template=test_template, description='')
    # Setup
    controller = JinjaAssertion(
        assertion_model=jinja_assertion_model,
        jinja_context=test_action_jinja_context,
        jinja_engine=test_run_time_jinja_engine,
    )
    # act
    controller.run()

    assert jinja_assertion_model.is_success == is_success
    assert jinja_assertion_model.state == AssertionStateEnum.EXECUTED

