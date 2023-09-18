import pytest

from api_compose.root.exceptions import ExecutionIdNonUniqueException
from api_compose.root.models.scenario import ScenarioModel
from api_compose.services.composition_service.models.actions.actions.http_actions import JsonHttpActionModel


def test_raise_error_when_actions_in_same_scenario_have_same_execution_ids():
    with pytest.raises(ExecutionIdNonUniqueException):
        action_one = JsonHttpActionModel(model_name='JsonHttpActionModel',id='some_id')
        action_two = JsonHttpActionModel(model_name='JsonHttpActionModel',id='some_other_id', execution_id='some_id')
        ScenarioModel(model_name='ScenarioModel',
            id='some_id',
            actions=[
                action_one,
                action_two,
            ]
        )

