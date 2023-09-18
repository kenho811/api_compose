import pytest

from api_compose.core.jinja.core.utils import extract_from_template_str


@pytest.mark.parametrize("template_str,expected_extracted_vars", [
    # can match
    (
            "{{ actions.login.output['token'] }}",
            ["actions.login.output['token']"],
    ),
    (
            "{{ hello.1.2.3 }} {{ bye.bye }}",
            [
                "hello.1.2.3",
                "bye.bye"
            ],

    )
])
def test_can_extract_from_template_str(template_str, expected_extracted_vars):
    actual_extracted_vars = extract_from_template_str(template_str)
    assert sorted(expected_extracted_vars) == sorted(actual_extracted_vars)
