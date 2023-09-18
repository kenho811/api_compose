import pytest

from api_compose.services.common.models.ref_resolver import RefResolverModel


@pytest.mark.parametrize(
    'ref_resolver_model,expected_description',
    [
        (RefResolverModel(model_name='RefResolverModel',description=' There are spaces      some where', context={}), 'there are spaces some where'),
    ]
)
def test_ref_resolver_description(
        ref_resolver_model,
        expected_description
):
    assert ref_resolver_model.description == expected_description


def test_null_id_and_description_raises_error(
):
    """Cannot have both id and description empty"""
    with pytest.raises(ValueError):
        RefResolverModel(model_name='RefResolverModel',context={})


def test_both_id_and_description_are_set_raises_error(
):
    """Cannot set both id and description"""
    with pytest.raises(ValueError):
        RefResolverModel(model_name='RefResolverModel',id='some_action.yaml', description='I goooo to sleep', context={})
