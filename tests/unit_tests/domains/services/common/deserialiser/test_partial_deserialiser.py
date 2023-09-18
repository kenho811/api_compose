from pathlib import Path

from api_compose import GlobalSettingsModelSingleton
from api_compose.services.common.deserialiser import get_models_description


def test_get_models_description(
        test_compile_time_jinja_engine,
        test_manifests_search_path,
):
    actual_dict = get_models_description(
        manifests_folder_path=test_manifests_search_path,
    )

    expected_subset = {
        'i can get image with positional execution id': Path('specifications/can_get_image_positional.yaml'),
        'i get image': Path('actions/get_image.yaml'),
        'i get other stuff': Path('actions/get_other_stuff.yaml')
    }

    for expected_key, expected_value in expected_subset.items():
        actual_value = actual_dict.get(expected_key)
        assert actual_value is not None, f"Expected Key {expected_key} not in actual {actual_dict}"
        assert actual_value == expected_value
