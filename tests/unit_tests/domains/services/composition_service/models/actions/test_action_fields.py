import pytest

from api_compose.core.utils.exceptions import ReservedKeywordsException
from api_compose.services.composition_service.models.actions.actions.http_actions import JsonHttpActionModel


@pytest.mark.parametrize(
    'action_model',
    [
        JsonHttpActionModel(id='action_id', model_name='JsonHttpActionModel', execution_id=''),
        JsonHttpActionModel(id='action_id', model_name='JsonHttpActionModel', execution_id=None),
    ]
)
def test_default_execution_id(action_model):
    """In case manifest gets a null value for execution_id """
    assert action_model.execution_id == action_model.id


def test_default_schemas_and_schema_validators():
    """In case manifest gets a null value for schemas or schema_validators """
    action_model = JsonHttpActionModel(id='action_id', model_name='JsonHttpActionModel', schemas=None,
                                       schema_validators=None)
    assert action_model.schemas == []
    assert action_model.schema_validators == []


def test_raise_validation_error_when_execution_id_is_self():
    """In case manifest gets a null value for schemas or schema_validators """
    with pytest.raises(ReservedKeywordsException):
        JsonHttpActionModel(id='self', model_name='JsonHttpActionModel', )
        JsonHttpActionModel(id='something_else', model_name='JsonHttpActionModel', execution_id='self')
