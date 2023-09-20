from pathlib import Path

import pytest

from api_compose.cli.session_builder import set_custom_selector_pack
from api_compose.core.settings.exceptions import IncludeExcludeBothSetException


def test_parse_models_raises_error_when_both_include_and_exclude_are_set(
        test_compile_time_jinja_engine,
        test_manifests_search_path,
):
    with pytest.raises(IncludeExcludeBothSetException):
        set_custom_selector_pack(
            include_manifest_file_paths=[Path('get_image')],
            include_tags=[],
            include_models=['SpecificationModel'],
            exclude_manifest_file_paths=[],
            exclude_tags=[],
            exclude_models=['JsonHttpActionModel'],
        )
