import pytest

from api_compose.core.utils.linear_graph import get_linear_execution_order, get_unique_list
from api_compose.core.utils.exceptions import CircularDependencyException, NonExistentNodeException


@pytest.mark.parametrize(
    'original_list,expected_list',
    [
        (
                [1,2,3,4],
                [1,2,3,4],
        ),
        (
                [1, 2, 3, 3],
                [1, 2, 3],
        ),
        (
                [1, 2, 2, 3],
                [1, 2, 3],
        ),

        (
                [1, 1, 1, 2],
                [1, 2],
        ),
    ]
)
def test_get_unique_list(original_list, expected_list):
    actual_list = get_unique_list(original_list)
    assert actual_list == expected_list


@pytest.mark.parametrize(
    'dependencies,expected_order',
    [
        (
                {'A': [], 'B': ['A']},
                ['A', 'B'],
        ),
        (
                {'A': [], 'B': ['A'], 'C': []},
                ['A', 'B', 'C'],
        ),
        (
                {'A': ['B', 'C'], 'B': ['D'], 'C': ['D', 'E'], 'D': ['E'], 'E': [], },
                ['E', 'D', 'B', 'C', 'A']
        )
    ]
)
def test_get_execution_order(dependencies, expected_order):
    actual_order = get_linear_execution_order(dependencies)
    assert actual_order == expected_order

@pytest.mark.parametrize(
    'dependencies',
    [
        (
            # self-depending node
                {'A': ['A'],}
        ),
        (
                # Circular dependence A -> B -> C -> A
                {'A': ['B'], 'B': ['C'], 'C': ['A'] }
        ),
    ]
)
def test_can_catch_circular_dependencies(dependencies):
    with pytest.raises(CircularDependencyException):
        get_linear_execution_order(dependencies)


@pytest.mark.parametrize(
    'dependencies',
    [
        (
                # Node B does not exist
                {'A': ['B'],}
        ),
    ]
)
def test_can_catch_non_existent_node(dependencies):
    with pytest.raises(NonExistentNodeException):
        get_linear_execution_order(dependencies)
