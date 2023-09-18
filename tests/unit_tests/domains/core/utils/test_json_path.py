import pytest

from api_compose.core.utils.exceptions import NoMatchesFoundForJsonPathException
from api_compose.core.utils.json_path import parse_json_with_jsonpath


@pytest.mark.parametrize(
    'deserialised_json,json_path,expected',
    [
        # standard
        ({'name': 'peter', 'gender': 'male', 'hobbies': ['basketball', 'football']},
         '$.name',
         'peter'),

        ({'name': 'peter', 'gender': 'male', 'hobbies': ['basketball', 'football']},
         '$.hobbies[1]',
         'football'
         ),

        # Get by checking other fields
        ({'entries': [{'name': 'peter', 'gender': 'male', 'hobbies': ['basketball', 'football']},
                      {'name': 'mary', 'gender': 'female', 'hobbies': ['drawing', 'singing']},
                      ]
          },
         "$.entries[?(@.gender == 'female')].name",
         'mary'
         ),

        ({'entries': [{'name': 'peter', 'gender': 'male', 'hobbies': ['basketball', 'football']},
                      {'name': 'mary', 'gender': 'female', 'hobbies': ['drawing', 'singing']},
                      ]
          },
         "$.entries[?(@.hobbies[*] == 'drawing')].name",
         'mary'
         ),

    ]
)
def test_parse_json_with_jsonpath_with_one_result_and_with_success(deserialised_json, json_path, expected):
    actual = parse_json_with_jsonpath(deserialised_json, json_path)
    assert actual == expected

@pytest.mark.parametrize(
    'deserialised_json,json_path,expected',
    [
        # standard
        ({'entries': [{'name': 'peter', 'gender': 'male', 'hobbies': ['basketball', 'football']},
                      {'name': 'sam', 'gender': 'male', 'hobbies': ['drinking', 'football']},
                      {'name': 'mary', 'gender': 'female', 'hobbies': ['drawing', 'singing']},
                      {'name': 'jane', 'gender': 'female', 'hobbies': ['football', 'shouting']},
                      ]
          },
         "$.entries[?(@.gender == 'male')].name",
         ['peter', 'sam'] ),

        # standard
        ({'entries': [{'name': 'peter', 'gender': 'male', 'hobbies': ['basketball', 'football']},
                      {'name': 'sam', 'gender': 'male', 'hobbies': ['drinking', 'football']},
                      {'name': 'mary', 'gender': 'female', 'hobbies': ['drawing', 'singing']},
                      {'name': 'jane', 'gender': 'female', 'hobbies': ['football', 'shouting']},
                      ]
          },
         "$.entries[?(@.hobbies[*] == 'football')].name",
         ['peter', 'sam', 'jane']),
    ]
)
def test_parse_json_with_jsonpath_with_all_results_and_with_success(deserialised_json, json_path, expected):
    actual = parse_json_with_jsonpath(deserialised_json, json_path, get_all_matches=True)
    assert actual == expected


@pytest.mark.parametrize(
    'deserialised_json,json_path',
    [
        ({'name': 'peter', 'gender': 'male', 'hobbies': ['basketball', 'football']},
         '$.not_exist'
         ),

        (None,
         '$.anything',
         ),

    ]
)
def test_parse_json_with_jsonpath_with_exception(deserialised_json, json_path):
    with pytest.raises(NoMatchesFoundForJsonPathException):
        parse_json_with_jsonpath(deserialised_json, json_path)
