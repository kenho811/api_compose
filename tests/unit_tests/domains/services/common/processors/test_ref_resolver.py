import pytest

from api_compose import GlobalSettingsModelSingleton
from api_compose.services.common.exceptions import ManifestIdNotFoundException, \
    ManifestDescriptionNotFoundException
from api_compose.services.common.models.ref_resolver import RefResolverModel
from api_compose.services.common.processors.ref_resolver import RefResolver


@pytest.mark.parametrize(
    'ref_resolver_model,expected_resolved_model_id',
    [
        # by ref id
        (RefResolverModel(model_name='RefResolverModel',ref='get_image', context={}), 'get_image'),

        # by description - GIVEN-WHEN-THEN
        (RefResolverModel(model_name='RefResolverModel',given='I get image', context={}), 'get_image'),
        (RefResolverModel(model_name='RefResolverModel',when='I Sleep for a while   ', context={}), 'sleep'),
        (RefResolverModel(model_name='RefResolverModel',then='I get other stuff', context={}), 'get_other_stuff'),

    ]
)
def test_ref_resolver_with_success(
        test_compile_time_jinja_engine,
        test_manifests_search_path,
        ref_resolver_model,
        expected_resolved_model_id
):
    ref_resolver_model.manifests_folder_path = test_manifests_search_path
    ref_resolver = RefResolver(
        ref_resolver_model=ref_resolver_model,
    )

    actual_model = ref_resolver.resolve()
    assert actual_model.id == expected_resolved_model_id


@pytest.mark.parametrize(
    'ref_resolver_model',
    [
        # by description - GIVEN-WHEN-THEN
        (RefResolverModel(model_name='RefResolverModel',given='I do not exist get image', context={})),
        (RefResolverModel(model_name='RefResolverModel',when='I do not exist get image', context={})),
        (RefResolverModel(model_name='RefResolverModel',then='I do not exist get image', context={})),

    ]
)
def test_ref_resolver_raise_manifest_not_found_by_description(
        test_compile_time_jinja_engine,
        test_manifests_search_path,
        ref_resolver_model,
):
    with pytest.raises(ManifestDescriptionNotFoundException):
        ref_resolver_model.manifests_folder_path = test_manifests_search_path
        RefResolver(
            ref_resolver_model=ref_resolver_model,
        ).resolve()
        
@pytest.mark.parametrize(
    'ref_resolver_model',
    [
        # by ref id
        (RefResolverModel(model_name='RefResolverModel',ref='not_exist', context={})),
    ]
)
def test_ref_resolver_raise_manifest_not_found_by_id_error(
        test_compile_time_jinja_engine,
        test_manifests_search_path,
        ref_resolver_model,
):
    with pytest.raises(ManifestIdNotFoundException):
        ref_resolver_model.manifests_folder_path = test_manifests_search_path
        RefResolver(
            ref_resolver_model=ref_resolver_model,
        ).resolve()
