from typing import Optional, List

import pytest

from api_compose.services.common.models.text_field.templated_text_field import JsonTemplatedTextField, StringTemplatedTextField
from api_compose.services.common.models.text_field.text_field import TextFieldFormatEnum
from api_compose.services.composition_service.models.actions.actions.base_action import BaseActionModel
from api_compose.services.composition_service.models.actions.actions.http_actions import JsonHttpActionModel
from api_compose.services.composition_service.models.actions.configs.http_configs import JsonHttpActionConfigModel
from api_compose.services.composition_service.models.actions.states import ActionStateEnum
from api_compose.services.persistence_service.processors.simple_backend import SimpleBackend


@pytest.fixture()
def parent_one_action_one_model(rest_base_url) -> JsonHttpActionModel:
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


@pytest.fixture()
def parent_two_action_one_model(rest_base_url) -> JsonHttpActionModel:
    return JsonHttpActionModel(model_name='JsonHttpActionModel',
        id='post_number_stateful',

        parent_ids=['test_suite_one', 'scenario_two'],
        description='Post Number Stateful',
        execution_id='post_number_stateful',
        config=JsonHttpActionConfigModel(
            url=StringTemplatedTextField(template=rest_base_url + '/unit/number/stateful-one', format=TextFieldFormatEnum.STRING),
            method=StringTemplatedTextField(template='POST', format=TextFieldFormatEnum.STRING),
            headers=JsonTemplatedTextField(template='{}', format=TextFieldFormatEnum.JSON),
            params=JsonTemplatedTextField(template='{}', format=TextFieldFormatEnum.JSON),
            body=JsonTemplatedTextField(template='{ "number": 20 }', format=TextFieldFormatEnum.JSON),
        ),
    )


@pytest.fixture()
def parent_two_action_two_model(rest_base_url) -> JsonHttpActionModel:
    return JsonHttpActionModel(model_name='JsonHttpActionModel',
        id='get_number_stateful',

        parent_ids=['test_suite_one', 'scenario_two'],
        description='Get Number Stateful',
        execution_id='get_number_stateful',
        config=JsonHttpActionConfigModel(
            url=StringTemplatedTextField(template=rest_base_url + '/unit/number/stateful-one', format=TextFieldFormatEnum.STRING),
            method=StringTemplatedTextField(template='GET', format=TextFieldFormatEnum.STRING),
            headers=JsonTemplatedTextField(template='{}', format=TextFieldFormatEnum.JSON),
            params=JsonTemplatedTextField(template='{}', format=TextFieldFormatEnum.JSON),
            body=JsonTemplatedTextField(template='{}', format=TextFieldFormatEnum.JSON),
        ),
    )


@pytest.fixture()
def populated_simple_backend(
        parent_one_action_one_model,
        parent_two_action_one_model,
        parent_two_action_two_model,
):
    sb = SimpleBackend()
    sb.add(parent_one_action_one_model)
    sb.add(parent_two_action_one_model)
    sb.add(parent_two_action_two_model)
    return sb


def test_can_get_saved_model_from_simple_backend(
        populated_simple_backend,
        parent_two_action_one_model):
    # Act
    actual = populated_simple_backend.get_latest_by_fqn(parent_two_action_one_model.fqn)
    expected = parent_two_action_one_model
    # Assert
    assert actual == expected


def test_can_get_latest_model_from_simple_backend(
        populated_simple_backend,
        parent_one_action_one_model
):
    # Act
    new_model = parent_one_action_one_model.model_copy(deep=True, update={
        '_state': ActionStateEnum.ENDED
    })
    populated_simple_backend.add(new_model)

    # assert
    actual: Optional[BaseActionModel] = populated_simple_backend.get_latest_by_fqn(
        parent_one_action_one_model.fqn)
    # Assert
    assert actual is not None
    assert type(actual) == JsonHttpActionModel
    assert actual._state == ActionStateEnum.ENDED


def test_can_get_multiple_actions_with_same_parent(
        populated_simple_backend,
        parent_two_action_two_model
):
    # assert
    actual: List[BaseActionModel] = populated_simple_backend.get_latest_siblings(
        parent_two_action_two_model)
    # Assert
    assert actual is not None and type(actual) == list and len(actual) == 2
