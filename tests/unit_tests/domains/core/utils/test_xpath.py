import pytest
from lxml import etree

from api_compose.core.utils.xpath import parse_xml_with_xpath


@pytest.mark.parametrize(
    'xml_str,xpath,expected',
    [
        ('<hello>1</hello>', '/hello/text()', '1')
    ]
)
def test_parse_xml_with_xpath(
        xml_str,
        xpath,
        expected
):
    actual = parse_xml_with_xpath(
        etree.fromstring(xml_str), xpath
    )
    assert actual == expected
