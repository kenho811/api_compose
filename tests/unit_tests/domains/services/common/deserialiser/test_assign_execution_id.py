from pathlib import Path

from api_compose.core.settings.settings import GlobalSettingsModelSingleton
from api_compose.root.models.scenario import ExecutionIdAssignmentEnum
from api_compose.root.models.specification import SpecificationModel
from api_compose.services.common.deserialiser.deserialiser import deserialise_manifest_to_model


def test_scenario_retains_execution_id(
        test_compile_time_jinja_engine,
        test_manifests_search_path,
):
    specification: SpecificationModel = deserialise_manifest_to_model(  # noqa
        manifest_file_path=Path('./specifications/can_get_image_user_defined.yaml'),
        manifests_folder_path=test_manifests_search_path,
    )

    scenarios = specification.scenarios
    for scenario in scenarios:
        if scenario.id == 'can_get_image':
            assert scenario.execution_id_assignment == ExecutionIdAssignmentEnum.UserDefined
            assert scenario.actions[0].execution_id == 'get_image'


def test_scenario_replaces_execution_id(
        test_compile_time_jinja_engine,
        test_manifests_search_path,
):
    specification: SpecificationModel = deserialise_manifest_to_model(  # noqa
        manifest_file_path=Path('./specifications/can_get_image_positional.yaml'),
        manifests_folder_path=test_manifests_search_path,
    )

    scenarios = specification.scenarios
    for scenario in scenarios:
        if scenario.id == 'can_get_image':
            assert scenario.execution_id_assignment == ExecutionIdAssignmentEnum.Positional
            assert scenario.actions[0].execution_id == '1'
