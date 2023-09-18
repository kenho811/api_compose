from pathlib import Path

from api_compose import GlobalSettingsModelSingleton
from api_compose.services.common.deserialiser.deserialiser import deserialise_manifest_to_model
from api_compose.services.composition_service.models.actions.actions.http_actions import JsonHttpActionModel


def test_can_deserialise_specification_manifest_to_model(
        test_compile_time_jinja_engine,
        test_manifests_search_path,
):
    deserialise_manifest_to_model(
        Path('./specifications/can_get_image_user_defined.yaml'),
        manifests_folder_path=test_manifests_search_path,
    )


def test_can_deserialise_action_manifest_to_model(
        test_compile_time_jinja_engine,
        test_manifests_search_path,
):
    model: JsonHttpActionModel = deserialise_manifest_to_model(  # noqa
        Path('./actions/get_image.yaml'),
        manifests_folder_path=test_manifests_search_path,
    )

    assert model.schemas[0].schema_.text

