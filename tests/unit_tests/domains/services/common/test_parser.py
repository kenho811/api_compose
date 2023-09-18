import pytest

from api_compose.services.common.deserialiser.parser import parse_string


@pytest.mark.parametrize(
    'string,expected',
    [
        # integer
        ('1234', 1234),

        # float
        ('1.1234', 1.1234),

        # string
        ('something', "something"),

        # boolean
        ('true', True),

    ]
)
def test_parse_string(string, expected):
    assert parse_string(string) == expected
