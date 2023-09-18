import pytest

from api_compose.cli.utils.parser import parse_context, convert_string


@pytest.mark.parametrize(
    'context,expected',
    [
        # No dots
        (None, {}),
        (['val=1'], {'val': 1}),
        (['val=stuff', 'val2=1.23'], {'val': 'stuff', 'val2': 1.23}),

        # dotted paths
        (['global=true', 'ns.obj_one=stuff', 'ns.obj_two=1.23'], {'global': True, 'ns': {'obj_one': 'stuff', 'obj_two': 1.23}}),
        (['global=true', 'global.obj_one=stuff', 'ns.obj_two=1.23'], {'global': True, 'ns': {'obj_two': 1.23}}),

    ]
)
def test_parse_context(context, expected):
    actual = parse_context(context)
    assert actual == expected


@pytest.mark.parametrize(
    'string,expected',
    [
        (None, None),
        ('12', 12),
        ('12.99', 12.99),
        ('True', True),
        ('true', True),
        ('false', False),
        ('stuff', 'stuff'),
    ]
)
def test_convert_string(string, expected):
    actual = convert_string(string)
    assert actual == expected
