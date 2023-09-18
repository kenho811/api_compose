import pytest

from api_compose.services.common.models.text_field.templated_text_field import StringTemplatedTextField, JsonTemplatedTextField
from api_compose.services.common.models.text_field.text_field import TextFieldFormatEnum
from api_compose.services.composition_service.models.actions.actions.http_actions import JsonHttpActionModel
from api_compose.services.composition_service.models.actions.configs.http_configs import JsonHttpActionConfigModel


@pytest.fixture()
def get_number_stateless_rest_action(rest_base_url) -> JsonHttpActionModel:
    return JsonHttpActionModel(model_name='JsonHttpActionModel',
        id='get_number_stateless',
        parent_ids=['test_suite_one', 'scenario_one'],
        description='Get Number',
        execution_id="get_number_stateless",
        config=JsonHttpActionConfigModel(
            url=StringTemplatedTextField(template=rest_base_url + '/unit/number/stateless', format=TextFieldFormatEnum.STRING),
            method=StringTemplatedTextField(template='GET', format=TextFieldFormatEnum.STRING),
            headers=JsonTemplatedTextField(template='{}', format=TextFieldFormatEnum.JSON),
            params=JsonTemplatedTextField(template='{}', format=TextFieldFormatEnum.JSON),
            body=JsonTemplatedTextField(template='{}', format=TextFieldFormatEnum.JSON),
        ),
    )
