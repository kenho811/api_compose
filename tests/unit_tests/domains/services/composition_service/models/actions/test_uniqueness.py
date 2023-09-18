import pytest

from api_compose.services.composition_service.models.actions.actions.http_actions import JsonHttpActionModel
from api_compose.services.composition_service.models.actions.outputs.http_outputs import JsonHttpActionOutputModel


def test_set_keep_one_model_only():
    """Actions with same execution_id get eliminated in a set"""
    action_model_one = JsonHttpActionModel(model_name='JsonHttpActionModel',id='same_action_id', output=JsonHttpActionOutputModel(url='http://abc.com'))
    action_model_two = JsonHttpActionModel(model_name='JsonHttpActionModel',id='same_action_id', output=JsonHttpActionOutputModel(url='http://xyz.com'))
    action_model_three = JsonHttpActionModel(model_name='JsonHttpActionModel',id='different_action_id')

    set_one = set()
    set_one.add(action_model_one)
    set_one.add(action_model_two)
    set_one.add(action_model_three)

    assert len(set_one) == 2