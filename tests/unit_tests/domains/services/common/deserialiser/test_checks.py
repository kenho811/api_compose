from pathlib import Path

import pytest

from api_compose.core.utils.files import are_files_unique_in, get_file_paths_relative_to, \
    is_folder_populated


def create_file(
        file_path: Path,
):
    parent = file_path.parent
    parent.mkdir(exist_ok=True, parents=True)
    with open(file_path, 'w') as f:
        f.write('stuff')


@pytest.fixture
def folder_with_no_files(
        tmp_path
):
    manifest_folder = tmp_path
    actions_folder = manifest_folder.joinpath('actions')
    specifications_folder = manifest_folder.joinpath('specifications')

    actions_folder.mkdir(parents=True, exist_ok=True)
    specifications_folder.mkdir(parents=True, exist_ok=True)

    return tmp_path


@pytest.fixture
def folder_with_identification_files(
        tmp_path
):
    manifest_folder = tmp_path
    actions_folder = manifest_folder.joinpath('actions')
    specifications_folder = manifest_folder.joinpath('specifications')

    create_file(actions_folder.joinpath('folder_one/action_one.yaml'))
    create_file(actions_folder.joinpath('folder_two/action_one.yaml'))
    create_file(actions_folder.joinpath('folder_three/action_two.yaml'))
    create_file(actions_folder.joinpath('folder_four/action_two.yaml'))
    create_file(actions_folder.joinpath('folder_five/action_three.yaml'))

    create_file(specifications_folder.joinpath('specification_one.yaml'))

    return tmp_path


@pytest.fixture
def folder_with_unique_files(
        tmp_path
):
    manifest_folder = tmp_path
    actions_folder = manifest_folder.joinpath('actions')
    actions_folder.mkdir()
    specifications_folder = manifest_folder.joinpath('specifications')
    specifications_folder.mkdir()

    create_file(actions_folder.joinpath('folder_one/action_one.yaml'))
    create_file(actions_folder.joinpath('folder_two/action_two.yaml'))
    create_file(actions_folder.joinpath('folder_three/action_three.yaml'))
    create_file(actions_folder.joinpath('folder_four/action_four.yaml'))
    create_file(actions_folder.joinpath('folder_five/action_five.yaml'))

    return tmp_path


def test_folder_with_no_files(
        folder_with_no_files
):
    actual = is_folder_populated(folder_with_no_files)
    assert not actual


def test_folder_with_files(
        folder_with_identification_files
):
    actual = is_folder_populated(folder_with_identification_files)
    assert actual


def test_folder_with_identical_files(
        folder_with_identification_files
):
    actual = are_files_unique_in(folder_with_identification_files)
    assert not actual


def test_folder_with_unique_files(
        folder_with_unique_files
):
    actual = are_files_unique_in(folder_with_unique_files)
    assert actual


def test_can_get_relative_path_if_exists(
        folder_with_unique_files,
):
    file_name = 'action_one'
    expected_file_paths = [Path('actions/folder_one/action_one.yaml')]
    actual_file_paths = get_file_paths_relative_to(folder_with_unique_files, file_name)

    assert actual_file_paths == expected_file_paths


def test_cannnot_get_relative_path_if_not_exists(
        folder_with_unique_files,
):
    file_name = 'some_nonexistent_action'
    actual_file_paths = get_file_paths_relative_to(folder_with_unique_files, file_name)
    assert len(actual_file_paths) == 0
