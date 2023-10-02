import json

import pytest

from api_compose.core.utils.exceptions import ReservedKeywordsException
from api_compose.services.common.models.text_field.templated_text_field import StringTemplatedTextField, \
    JsonTemplatedTextField
from api_compose.services.common.registry.jinja_function_registry import FunctionsRegistry, FunctionType
from api_compose.services.composition_service.jinja.context import ActionJinjaContext
from api_compose.services.composition_service.models.actions.actions.http_actions import JsonHttpActionModel
from api_compose.services.composition_service.models.actions.configs.http_configs import JsonHttpActionConfigModel
from api_compose.services.composition_service.processors.adapters.http_adapter.json_http_adapter import JsonHttpAdapter



def test_adapter_throws_reserved_keywords_exception(
        start_rest_server,
        rest_base_url,
        test_run_time_jinja_engine,
):
    current_action_model = JsonHttpActionModel(model_name='JsonHttpActionModel',
        id='get_number_stateless',
        parent_ids=['test_suite_one', 'scenario_one'],
        description='Get Number',
        execution_id="get_number_stateless",
        config=JsonHttpActionConfigModel(
            url=StringTemplatedTextField(template=rest_base_url + '/unit/number/stateless'),
            method=StringTemplatedTextField(template='GET'),
            headers=JsonTemplatedTextField(template='{}'),
            params=JsonTemplatedTextField(template='{}'),
            body=JsonTemplatedTextField(template='{}'),
        ),
        pre_hook_context={
            # Using reserved keywords
            'action_models': "{{ get_one() }}"
        }
    )

    processor = JsonHttpAdapter(
        jinja_engine=test_run_time_jinja_engine,
        action_model=current_action_model,
    )

    processor.start(jinja_context=ActionJinjaContext(current_action_model=current_action_model))
    processor.stop()

    assert type(current_action_model._exec) == ReservedKeywordsException


def test_different_config_fields_can_reference_same_variable_in_prehook(
        start_rest_server,
        rest_base_url,
        test_run_time_jinja_engine,
):
    current_action_model = JsonHttpActionModel(model_name='JsonHttpActionModel',
        id='get_number_stateless',
        parent_ids=['test_suite_one', 'scenario_one'],
        description='Get Number',
        execution_id="get_number_stateless",
        config=JsonHttpActionConfigModel(
            url=StringTemplatedTextField(template=rest_base_url + '/unit/number/stateless'),
            method=StringTemplatedTextField(template='GET'),
            headers=JsonTemplatedTextField(template='{}'),
            params=JsonTemplatedTextField(template=json.dumps({'query': '{{ one }}'})),
            body=JsonTemplatedTextField(template=json.dumps({'some_field': '{{ one }}'}))
        ),
        pre_hook_context={
            # Using reserved keywords
            'one': "{{ get_one() }}"
        }
    )

    processor = JsonHttpAdapter(
        jinja_engine=test_run_time_jinja_engine,
        action_model=current_action_model,
    )

    processor.start(jinja_context=ActionJinjaContext(current_action_model=current_action_model))
    processor.stop()

    assert current_action_model.config.params.obj == {'query': '1'}
    assert current_action_model.config.body.obj == {'some_field': '1'}
