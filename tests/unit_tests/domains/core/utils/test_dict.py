import pytest

from api_compose.core.utils.dict import count_items, merge_dict


@pytest.mark.parametrize(
    'item,expected',
    [
        (
                {
                    'key1': 'value1',
                    'key2': {
                        'subkey1': 'subvalue1',
                        'subkey2': 'subvalue2',
                        'subkey3': ['as', 'as']
                    },
                    'key3': {
                        'subkey3': {
                            'subsubkey1': 'subsubvalue1'
                        }
                    }
                },
            6
        )
    ]
)
def test_count_items(item,expected):
    actual =  count_items(item)
    assert actual == expected


@pytest.mark.parametrize(
    'overlayed_dict,overlaying_dict,expected_dict',
    [
        # Overlaying Dict replaces field in overlayed dict
        ({"fruits": {'apple': {'weight': 12, 'is_fresh': True}}},
         {"fruits": {'apple': {'weight': 20}}},
         {"fruits": {'apple': {'weight': 20, 'is_fresh': True}}},),

        # If the overlayed field is a list, the whole list is replaced
        ({"fruits": ['apple', 'pineapple']},
         {"fruits": ['orange']},
         {"fruits": ['orange']}),

        # Additional fields in overlaying_dict are added to the overlayed dict
        ({"fruits": "apple"},
         {"fruits": "banana", "drinks": 'beer'},
         {"fruits": "banana", "drinks": "beer"}),
    ]
)
def test_merge_dict(overlayed_dict, overlaying_dict, expected_dict):
    _original_dict = overlayed_dict.copy()
    _replace_dict = overlaying_dict.copy()

    actual_dict = merge_dict(overlayed_dict, overlaying_dict)

    assert _original_dict == overlayed_dict
    assert _replace_dict == overlaying_dict
    assert actual_dict == expected_dict
