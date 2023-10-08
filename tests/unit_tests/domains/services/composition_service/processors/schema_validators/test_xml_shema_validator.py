import json
from typing import List

import pytest
from lxml import etree

from api_compose.core.lxml.parser import get_parser
from api_compose.services.common.models.text_field.text_field import JsonTextField, XmlTextField
from api_compose.services.common.registry.processor_registry import ProcessorRegistry
from api_compose.services.composition_service.models.actions.outputs.http_outputs import XmlHttpActionOutputModel
from api_compose.services.composition_service.models.actions.schemas import JsonSchemaModel, XmlSchemaModel, \
    BaseSchemaModel
from api_compose.services.composition_service.models.schema_validatiors.schema_validators import \
    XmlSchemaValidatorModel, JsonSchemaValidatorModel
from api_compose.services.composition_service.processors.schema_validators.xml_schema_validator import \
    XmlSchemaValidator


@pytest.fixture()
def xml_action_output_model():
    return XmlHttpActionOutputModel(
        url='http://helloworld.com?is_xml=true',
        status_code=200,
        headers={'Server': 'nginx/1.18.0 (Ubuntu)',
                 'Date': 'Mon, 18 Sep 2023 12:05:35 GMT',
                 'Content-Type': 'application/xml; charset=utf-8',
                 'Transfer-Encoding': 'chunked',
                 'Connection': 'keep-alive',
                 'X-Frame-Options': 'SAMEORIGIN',
                 'X-XSS-Protection': '1; mode=block',
                 'X-Content-Type-Options': 'nosniff',
                 'X-Download-Options': 'noopen',
                 'X-Permitted-Cross-Domain-Policies': 'none',
                 'Referrer-Policy': 'strict-origin-when-cross-origin',
                 'ETag': 'W/"2f64c8d67ebd6279071b3baaf80d4d41"',
                 'Cache-Control': 'max-age=0, private, must-revalidate',
                 'X-Request-Id': '5ce9af95-2093-47b5-857e-cb40b2d0fcf5',
                 'X-Runtime': '0.007676',
                 'Strict-Transport-Security': 'max-age=31536000; includeSubDomains, max-age=15768000',
                 'Vary': 'Origin'
                 },
        body=etree.fromstring(
            b'''<?xml version="1.0" encoding="UTF-8"?>
<objects type="array">
    <object>
        <id type="integer">369</id>
        <uid>f4328099-4aa7-4e19-86e9-f7b94458b39a</uid>
        <password>Wr6RntQ04m</password>
        <first-name>Dave</first-name>
        <last-name>McClure</last-name>
        <username>dave.mcclure</username>
        <email>dave.mcclure@email.com</email>
        <avatar>https://robohash.org/quoconsecteturdolore.png?size=300x300&amp;set=set1</avatar>
        <gender>Non-binary</gender>
        <phone-number>+64 172-959-0081 x87362</phone-number>
        <social-insurance-number>560354383</social-insurance-number>
        <date-of-birth type="date">1973-03-31</date-of-birth>
        <employment>
            <title>Product Advertising Developer</title>
            <key-skill>Communication</key-skill>
        </employment>
        <address>
            <city>Andersonhaven</city>
            <street-name>Schultz Drive</street-name>
            <street-address>7895 Donny Mountains</street-address>
            <zip-code>39874-2440</zip-code>
            <state>Louisiana</state>
            <country>United States</country>
            <coordinates>
                <lat type="float">71.27012438895736</lat>
                <lng type="float">35.74794378636244</lng>
            </coordinates>
        </address>
        <credit-card>
            <cc-number>6771-8922-7052-8551</cc-number>
        </credit-card>
        <subscription>
            <plan>Professional</plan>
            <status>Active</status>
            <payment-method>Cheque</payment-method>
            <term>Payment in advance</term>
        </subscription>
    </object>
</objects>''',
            parser=get_parser())
    )


@pytest.fixture()
def schema_models() -> List[BaseSchemaModel]:
    return [
        JsonSchemaModel(
            model_name='JsonSchemaModel',
            id='200_json',
            schema_=JsonTextField(
                text=json.dumps(
                    {
                        "$schema": "http://json-schema.org/draft-07/schema#",
                        "type": "object",
                        "properties": {
                            "X-Request-Id": {
                                "type": "string",
                                "pattern": "^[a-zA-Z0-9]+-[a-zA-Z0-9]+-[a-zA-Z0-9]+-[a-zA-Z0-9]+-[a-zA-Z0-9]+$"
                            }
                        },
                        "required": ["X-Request-Id"]
                    },
                )
            )
        ),
        XmlSchemaModel(
            model_name='XmlSchemaModel',
            id='200_xml',
            schema_=XmlTextField(
                text="""<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="objects">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="object" maxOccurs="unbounded">
          <xs:complexType>
            <xs:sequence>
              <xs:element name="id" type="xs:integer"/>
              <xs:element name="uid" type="xs:string"/>
              <xs:element name="password" type="xs:string"/>
              <xs:element name="first-name" type="xs:string"/>
              <xs:element name="last-name" type="xs:string"/>
              <xs:element name="username" type="xs:string"/>
              <xs:element name="email" type="xs:string"/>
              <xs:element name="avatar" type="xs:string"/>
              <xs:element name="gender" type="xs:string"/>
              <xs:element name="phone-number" type="xs:string"/>
              <xs:element name="social-insurance-number" type="xs:integer"/>
              <xs:element name="date-of-birth" type="xs:date"/>
              <xs:element name="employment">
                <xs:complexType>
                  <xs:sequence>
                    <xs:element name="title" type="xs:string"/>
                    <xs:element name="key-skill" type="xs:string"/>
                  </xs:sequence>
                </xs:complexType>
              </xs:element>
              <xs:element name="address">
                <xs:complexType>
                  <xs:sequence>
                    <xs:element name="city" type="xs:string"/>
                    <xs:element name="street-name" type="xs:string"/>
                    <xs:element name="street-address" type="xs:string"/>
                    <xs:element name="zip-code" type="xs:string"/>
                    <xs:element name="state" type="xs:string"/>
                    <xs:element name="country" type="xs:string"/>
                    <xs:element name="coordinates">
                      <xs:complexType>
                        <xs:sequence>
                          <xs:element name="lat" type="xs:float"/>
                          <xs:element name="lng" type="xs:float"/>
                        </xs:sequence>
                      </xs:complexType>
                    </xs:element>
                  </xs:sequence>
                </xs:complexType>
              </xs:element>
              <xs:element name="credit-card">
                <xs:complexType>
                  <xs:sequence>
                    <xs:element name="cc-number" type="xs:string"/>
                  </xs:sequence>
                </xs:complexType>
              </xs:element>
              <xs:element name="subscription">
                <xs:complexType>
                  <xs:sequence>
                    <xs:element name="plan" type="xs:string"/>
                    <xs:element name="status" type="xs:string"/>
                    <xs:element name="payment-method" type="xs:string"/>
                    <xs:element name="term" type="xs:string"/>
                  </xs:sequence>
                </xs:complexType>
              </xs:element>
            </xs:sequence>
          </xs:complexType>
        </xs:element>
      </xs:sequence>
      <xs:attribute name="type" type="xs:string"/>
    </xs:complexType>
  </xs:element>
</xs:schema>""",
            )
        )
    ]


@pytest.mark.parametrize(
    'schema_validator_model',
    [
        (
                XmlSchemaValidatorModel(
                    model_name='XmlSchemaValidatorModel',
                    id='200_body_xml',
                    schema_id='200_xml',
                    against='output_body',
                )
        ),

        (
                JsonSchemaValidatorModel(
                    model_name='JsonSchemaValidatorModel',
                    id='200_headers_json',
                    schema_id='200_json',
                    against='output_headers',
                )
        ),

    ]
)
def test_mixed_schema_validator(
        schema_models,
        xml_action_output_model,
        schema_validator_model,
):
    schema_validator = ProcessorRegistry.create_processor_by_name(
        class_name=schema_validator_model._class_name,
        config={'schema_models': schema_models,
                'action_output_model': xml_action_output_model,
                'schema_validator_model': schema_validator_model,
                }
    )

    schema_validator.validate()

    assert schema_validator_model.is_valid and schema_validator_model.exec is None, schema_validator_model.exec
