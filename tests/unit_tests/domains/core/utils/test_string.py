import pytest

from api_compose.core.utils.string import split_pascal_case_string, convert_dotted_string_to_nested_dict, \
    normalise_sentence, convert_keys_in_nested_dict_to_dotted_paths


@pytest.mark.parametrize(
    'string,expected',
    [
        ('SomeClassName',
         ['Some', 'Class', 'Name'],
         ),

        ('alllowercase',
         ['alllowercase'],
         ),

        ('someUppercase',
         ['some', 'Uppercase'],
         )

    ]
)
def test_split_pascal_case_string(string, expected):
    actual = split_pascal_case_string(string)
    assert actual == expected


@pytest.mark.parametrize(
    'pairs,expected',
    [
        ([('a.b', 12), ('a.c', 90)], {'a': {'b': 12, 'c': 90}}),

        # First item prevents nested dict
        ([('a', 'occupied'), ('a.b', 'not_exist_one'), ('a.c', 'not_exist_two')], {'a': 'occupied'}),

        # last item prevents nested dict
        ([('a.b', 'not_exist_one'), ('a.c', 'not_exist_two'), ('a', 'occupied')], {'a': 'occupied'}),
    ]
)
def test_convert_dotted_string_to_nested_dict(pairs, expected):
    actual = convert_dotted_string_to_nested_dict(pairs)
    assert actual == expected


@pytest.mark.parametrize(
    'dict_,expected',
    [
        ({'k1': 'v1'}, ['k1']),

        ({'k1': 'v1', 'k2': 'v2'}, ['k1', 'k2']),

        ({'k1': {'sub_k1': []}, 'k2': 'v2'}, ['k1.sub_k1', 'k2']),

        ({}, []),

        ([], []),
    ]
)
def test_convert_keys_in_nested_dict_to_dotted_paths(dict_, expected):
    actual = convert_keys_in_nested_dict_to_dotted_paths(dict_)
    assert actual == expected


@pytest.mark.parametrize(
    'sentence,expected',
    [
        # case
        ('I create order', 'i create order'),

        # case and space
        ('      I   CANCEL     ORDER     ', 'i cancel order'),

        # case, space, punctuation
        ('   ,,,   I   CANCEL     ORDER !!!!!! .....      ', 'i cancel order'),

    ]

)
def test_normalise_sentence(
        sentence,
        expected
):
    actual = normalise_sentence(sentence)
    assert actual == expected
