import time
from typing import List, Union

import pytest
from pydantic import BaseModel as _BaseModel

from api_compose.core.utils.base_scheduler import BaseScheduler


class MockModel(_BaseModel):
    id: int
    is_done: bool = False


@pytest.fixture()
def mock_execution_seconds():
    return 0.5


@pytest.fixture()
def rescan_all_nodes_in_seconds():
    return 0.5


class MockScheduler(BaseScheduler):

    def __init__(self,
                 execution_seconds: Union[int, float],
                 *args,
                 **kwargs,
                 ):
        super().__int__(*args, **kwargs)
        self.execute_seconds = execution_seconds

    def is_node_done(self, node: MockModel) -> bool:
        return node.is_done

    def is_node_successful(self, node: MockModel) -> bool:
        return node.is_done

    def execute_node(self, node: MockModel, skip: bool) -> None:
        print(f'executing {node.id=}. Start time: {time.time()}. Going to take {self.execute_seconds=}')
        time.sleep(self.execute_seconds)
        node.is_done = True
        print(f'Done {node.id=}. End time: {time.time()}')


def convert_id_to_mock_models(id, mock_models: List[MockModel]) -> MockModel:
    for mock_model in mock_models:
        if mock_model.id == id:
            return mock_model


@pytest.mark.parametrize(
    'edges_ids,expected_independent_node_execution_num',
    [
        # Strict sequential execution
        ([(1, 2), (2, 3)], 3),
        # Strict parallel exeuction
        ([], 1),
        # partial parallel exeuction
        ([(1, 2)], 2),

    ]
)
def test_sequential_execution(
        mock_execution_seconds,
        rescan_all_nodes_in_seconds,

        edges_ids,
        expected_independent_node_execution_num,
):
    print(
        f"Each node takes {mock_execution_seconds=} seconds. Each rescan takes {rescan_all_nodes_in_seconds=} seconds")
    mock_model_1 = MockModel(id=1)
    mock_model_2 = MockModel(id=2)
    mock_model_3 = MockModel(id=3)

    mock_models = [mock_model_1, mock_model_2, mock_model_3]
    edges = [(convert_id_to_mock_models(edge_id_1, mock_models), convert_id_to_mock_models(edge_id_2, mock_models)) for
             (edge_id_1, edge_id_2) in edges_ids]

    start_time = time.time()
    scheduler = MockScheduler(
        execution_seconds=mock_execution_seconds,
        max_concurrent_node_execution_num=10,
        rescan_all_nodes_in_seconds=rescan_all_nodes_in_seconds,
        nodes=mock_models,
        edges=edges,
    )
    scheduler.run()
    end_time = time.time()

    total_elapsed_seconds = end_time - start_time
    expected_time_elapsed_lower_bound = mock_execution_seconds * expected_independent_node_execution_num
    expected_time_elapsed_upper_bound = expected_time_elapsed_lower_bound + rescan_all_nodes_in_seconds * expected_independent_node_execution_num

    print('======== Statistics ========')
    print(f"{total_elapsed_seconds=}")
    print(f"{expected_time_elapsed_lower_bound=}")
    print(f"{expected_time_elapsed_upper_bound=}")

    assert all([model.is_done for model in mock_models])

    assert total_elapsed_seconds >= expected_time_elapsed_lower_bound, f'Time elapsed is expected to be greater than {expected_time_elapsed_lower_bound=} seconds'
    assert total_elapsed_seconds <= expected_time_elapsed_upper_bound, f'Time elapsed is expected to be less than {expected_time_elapsed_upper_bound=} seconds'
