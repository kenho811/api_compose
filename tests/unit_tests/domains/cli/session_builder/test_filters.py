from pathlib import Path
from typing import List

import pytest

from api_compose.cli.session_builder import filter_by_inclusion, filter_by_exclusion
from api_compose.root.models.specification import SpecificationModel
from api_compose.services.common.models.base import BaseModel
from api_compose.services.composition_service.models.actions.actions.http_actions import JsonHttpActionModel, \
    XmlHttpActionModel


@pytest.fixture()
def models() -> List[BaseModel]:
    return [
        JsonHttpActionModel(model_name='JsonHttpActionModel',
            id='json_http_action_one',
            tags={'smoke_test', 'qa'},
            manifest_file_path='actions/json_http_action_one.yaml',
        ),

        JsonHttpActionModel(model_name='JsonHttpActionModel',
            id='json_http_action_two',
            tags={'regression', 'qa'},
            manifest_file_path='actions/json_http_action_two.yaml',
        ),

        XmlHttpActionModel(model_name='XmlHttpActionModel',
            id='xml_http_action_one',
            tags={'regression', 'qa'},
            manifest_file_path='actions/xml_http_action_one.yaml',
        ),

        SpecificationModel(model_name='SpecificationModel',
            id='specification_one',
            tags={'end_to_end'},
            manifest_file_path='specifications/specification_one.yaml',
            scenarios=[]
        )
    ]


@pytest.mark.parametrize(
    'include_manifest_file_paths,include_tags,include_models,expected_ids',
    [
        ([Path('actions/json_http_action_one.yaml')], set(), [], ['json_http_action_one']),
        ([Path('actions/json_http_action_one.yaml'), Path('actions/json_http_action_two.yaml')], set(), [],
         ['json_http_action_one', 'json_http_action_two']),
        (
        [Path('actions/json_http_action_one.yaml')], {'end_to_end'}, [], ['json_http_action_one', 'specification_one']),
        ([], {'qa'}, [], ['json_http_action_one', 'json_http_action_two', 'xml_http_action_one']),
        ([], {}, ['XmlHttpActionModel'], ['xml_http_action_one']),
        ([], {}, ['XmlHttpActionModel', 'SpecificationModel'], ['xml_http_action_one', 'specification_one']),
    ]
)
def test_filter_by_inclusion(
        models,
        include_manifest_file_paths,
        include_tags,
        include_models,
        expected_ids
):
    actual_models = filter_by_inclusion(
        models=models,
        include_manifest_file_paths=include_manifest_file_paths,
        include_tags=include_tags,
        include_models=include_models,
    )

    assert sorted([model.id for model in actual_models]) == sorted(expected_ids)


@pytest.mark.parametrize(
    'exclude_manifest_file_paths,exclude_tags,exclude_models,expected_ids',
    [
        ([Path('actions/json_http_action_one.yaml')], [], [],
         ['json_http_action_two', 'xml_http_action_one', 'specification_one']),
        ([Path('actions/json_http_action_one.yaml'), Path('actions/json_http_action_two.yaml')], set(), [],
         ['xml_http_action_one', 'specification_one']),
        ([Path('actions/json_http_action_one.yaml')], {'end_to_end'}, [],
         ['json_http_action_two', 'xml_http_action_one']),
        ([], ['qa'], [], ['specification_one']),
        ([], {}, ['XmlHttpActionModel'], ['json_http_action_one', 'json_http_action_two', 'specification_one']),
        ([], {}, ['XmlHttpActionModel', 'SpecificationModel'], ['json_http_action_one', 'json_http_action_two']),
    ]
)
def test_filter_by_exclusion(
        models,
        exclude_manifest_file_paths,
        exclude_tags,
        exclude_models,
        expected_ids
):
    actual_models = filter_by_exclusion(
        models=models,
        exclude_manifest_file_paths=exclude_manifest_file_paths,
        exclude_tags=exclude_tags,
        exclude_models=exclude_models,
    )

    assert sorted([model.id for model in actual_models]) == sorted(expected_ids)
