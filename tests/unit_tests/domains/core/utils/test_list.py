import pytest

from api_compose.core.utils.list import get_duplicates_in_list


@pytest.mark.parametrize(
    'test_list,expected',
    [
        (
                [1, 5, 2, 1, 4, 5, 1],
                [1,5]
        ),
        (
                ['a', 'b', 'c'],
                [],
        )

    ]
)
def test_get_duplicates_in_list(
        test_list,
        expected,
):
    actual = get_duplicates_in_list(test_list)
    assert actual.sort() == expected.sort()
