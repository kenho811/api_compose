import pytest
from lxml import etree

from api_compose.services.common.models.text_field.templated_text_field import StringTemplatedTextField, JsonTemplatedTextField, YamlTemplatedTextField, XmlTemplatedTextField
from api_compose.services.common.models.text_field.text_field import TextFieldFormatEnum


## String
@pytest.fixture
def test_string_templated_field() -> StringTemplatedTextField:
    return StringTemplatedTextField(
        template="{{ action('get_image') | output_body| jpath('$.val') }}",
        format=TextFieldFormatEnum.STRING
    )


def test_render_string_templated_field(
        test_run_time_jinja_engine,
        test_action_jinja_context,
        test_string_templated_field
):
    actual: StringTemplatedTextField = test_string_templated_field.render_to_text(test_run_time_jinja_engine, test_action_jinja_context).deserialise_to_obj()
    assert actual.obj == "12"


## JSON
@pytest.fixture
def test_json_templated_field() -> JsonTemplatedTextField:
    return JsonTemplatedTextField(
        template="""
        { {% for i in range(3) %}
          "some_url_{{ i }}" : "{{ action('get_image')| input_url }}",
          {% endfor %}
          "some_val": {{ action('get_image')| output_body| jpath('$.val') }},
          "some_val_str": "{{ action('get_image')| output_body| jpath('$.val') }}",
          "some_bool": false,
          "some_null": null
           }
         """,
        format=TextFieldFormatEnum.JSON
    )


def test_render_and_load_json_templated_field(test_run_time_jinja_engine, test_action_jinja_context, test_json_templated_field):
    actual: JsonTemplatedTextField = test_json_templated_field.render_to_text(test_run_time_jinja_engine, test_action_jinja_context).deserialise_to_obj()
    assert actual.obj == {
        'some_url_0': 'http://abc.com/v1/images',
        'some_url_1': 'http://abc.com/v1/images',
        'some_url_2': 'http://abc.com/v1/images',
        'some_val': 12,
        'some_val_str': "12",
        "some_bool": False,
        "some_null": None
    }


## YAML
@pytest.fixture()
def test_yaml_templated_field() -> YamlTemplatedTextField:
    return YamlTemplatedTextField(
        # indentation
        template=r"""
{%- for i in range(3) %}
"some_url_{{ i }}": "{{  action('get_image') | input_url  }}"
{%- endfor %}
"some_val":
    "some_val": {{ action('get_image') | output_body| jpath('$.val') }}
"some_bool": false
"some_null": null
        """,
        format=TextFieldFormatEnum.YAML
    )


def test_render_yaml_templated_field(test_run_time_jinja_engine, test_action_jinja_context, test_yaml_templated_field):
    templated_field: YamlTemplatedTextField = test_yaml_templated_field.render_to_text(test_run_time_jinja_engine, test_action_jinja_context).deserialise_to_obj()
    assert templated_field.obj == {
        'some_url_0': 'http://abc.com/v1/images',
        'some_url_1': 'http://abc.com/v1/images',
        'some_url_2': 'http://abc.com/v1/images',
        'some_val': {
            "some_val": 12,
        },
        "some_bool": False,
        "some_null": None

    }

## YAML
@pytest.fixture
def test_xml_templated_field():
    return XmlTemplatedTextField(
        # indentation
        template=r"""
            <urls>
                {%- for i in range(3) %}
                  <some_url_{{ i }}> {{  action('get_image')| input_url  }} </some_url_{{ i }}>
                {%- endfor %}
            </urls> 
       """,
        format=TextFieldFormatEnum.XML
    )


def test_render_xml_templated_field(test_run_time_jinja_engine, test_action_jinja_context, test_xml_templated_field):
    actual: XmlTemplatedTextField = test_xml_templated_field.render_to_text(test_run_time_jinja_engine, test_action_jinja_context).deserialise_to_obj()
    expected = etree.fromstring("""
            <urls>
                  <some_url_0> http://abc.com/v1/images </some_url_0>
                  <some_url_1> http://abc.com/v1/images </some_url_1>
                  <some_url_2> http://abc.com/v1/images </some_url_2>
            </urls> 
    """)
    assert actual.text == etree.tostring(expected).decode()
