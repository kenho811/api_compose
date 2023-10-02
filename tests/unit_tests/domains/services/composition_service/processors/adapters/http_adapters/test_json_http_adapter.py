import json

import pytest

from api_compose import JsonHttpAdapter
from api_compose.services.common.models.text_field.templated_text_field import StringTemplatedTextField, \
    JsonTemplatedTextField
from api_compose.services.common.models.text_field.text_field import TextFieldFormatEnum
from api_compose.services.composition_service.jinja.context import ActionJinjaContext
from api_compose.services.composition_service.models.actions.actions.http_actions import JsonHttpActionModel
from api_compose.services.composition_service.models.actions.configs.http_configs import JsonHttpActionConfigModel
from api_compose.services.composition_service.models.actions.states import ActionStateEnum
from api_compose.services.composition_service.models.protocols.status_enums import HttpResponseStatusEnum


@pytest.mark.parametrize(
    'endpoint,method,headers,body,params,expected_json_body,expected_status_code,expected_response_status',
    [
        (
                '/unit/number/stateless',
                StringTemplatedTextField(template='GET', format=TextFieldFormatEnum.STRING),
                JsonTemplatedTextField(template='{}', format=TextFieldFormatEnum.JSON),
                JsonTemplatedTextField(template='{}', format=TextFieldFormatEnum.JSON),
                JsonTemplatedTextField(template=json.dumps({'number': 15}), format=TextFieldFormatEnum.JSON),
                {'number': 15},
                200,
                HttpResponseStatusEnum.OK,
        ),

        (
                '/unit/number/stateless',
                StringTemplatedTextField(template='GET', format=TextFieldFormatEnum.STRING),
                JsonTemplatedTextField(template='{}', format=TextFieldFormatEnum.JSON),
                JsonTemplatedTextField(template='{}', format=TextFieldFormatEnum.JSON),
                JsonTemplatedTextField(template=json.dumps({'number': 'abcde'}), format=TextFieldFormatEnum.JSON),
                {'detail': "Wrong type, expected 'integer' for query parameter 'number'",
                 'status': 400,
                 'title': 'Bad Request',
                 'type': 'about:blank'},
                400,
                HttpResponseStatusEnum.BAD_REQUEST,
        ),

    ]
)
def test_number_stateless_returns_bac_request_with_wrong_body_data_type(
        start_api_server_two,
        rest_base_url,
        test_run_time_jinja_engine,
        endpoint,
        method,
        headers,
        body,
        params,
        expected_json_body,
        expected_status_code,
        expected_response_status
):
    current_action_model = JsonHttpActionModel(model_name='JsonHttpActionModel',
        id='get_number_stateless',
        parent_ids=['test_suite_one', 'scenario_one'],
        description='Get Number',
        execution_id="get_number_stateless",
        config=JsonHttpActionConfigModel(
            url=StringTemplatedTextField(template=rest_base_url + endpoint),
            method=method,
            headers=headers,
            body=body,
            params=params,
        )
    )
    adapter = JsonHttpAdapter(
        jinja_engine=test_run_time_jinja_engine,
        action_model=current_action_model,
    )

    adapter.start(jinja_context=ActionJinjaContext(current_action_model=current_action_model, ))
    adapter.stop()

    assert current_action_model.output.body == expected_json_body
    assert current_action_model.output.status_code == expected_status_code
    assert current_action_model.response_status == expected_response_status
    assert current_action_model.state == ActionStateEnum.ENDED


