from pathlib import Path

import pytest

from api_compose.services.common.env import render_load_and_merge_templated_yamls_as_single_dict


@pytest.mark.parametrize(
    'yaml_paths,expected',
    [
        # Test self-reference global
        ([Path('yaml-one.yaml')],
         {'global': 'global_string', 'field_one': {'sub_field_one': 1, 'sub_field_two': 'global_string'}}),

        # Test overlay yamls
        ([Path('yaml-one.yaml'), Path('yaml-two.yaml')],
         {'global': 'global_string', 'field_one': {'sub_field_one': {'sub_sub_field_one': 'another_value'}, 'sub_field_two': 'global_string'}}),

        # Test overlay yamls - reverse order
        ([Path('yaml-two.yaml'), Path('yaml-one.yaml')],
         {'global': 'global_string',
          'field_one': {'sub_field_one': 1, 'sub_field_two': 'global_string'}}),
    ]
)
def test_env_vars(
        test_compile_time_jinja_engine,
        yaml_paths,
        expected
):
    actual = render_load_and_merge_templated_yamls_as_single_dict(
        yaml_file_paths=[Path(__file__).parent.joinpath(yaml_path) for yaml_path in yaml_paths],
        jinja_engine=test_compile_time_jinja_engine,
    )
    assert actual == expected
