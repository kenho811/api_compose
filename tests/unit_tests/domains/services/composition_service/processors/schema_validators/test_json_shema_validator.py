import json

import pytest

from api_compose.services.common.models.text_field.text_field import JsonTextField
from api_compose.services.composition_service.models.actions.outputs.http_outputs import JsonHttpActionOutputModel
from api_compose.services.composition_service.models.actions.schemas import JsonSchemaModel
from api_compose.services.composition_service.models.schema_validatiors.schema_validators import \
    JsonSchemaValidatorModel
from api_compose.services.composition_service.processors.schema_validators.json_schema_validator import \
    JsonSchemaValidator


@pytest.fixture()
def json_action_output_model():
    return JsonHttpActionOutputModel(
        url='http://helloworld.com',
        status_code=200,
        headers={
            'x-dns-prefetch-control': 'off',
            'x-frame-options': 'SAMEORIGIN',
            'strict-transport-security': 'max-age=15552000; includeSubDomains',
            'x-download-options': 'noopen',
            'x-content-type-options': 'nosniff',
            'x-xss-protection': '1; mode=block',
            'vary': 'Origin',
            'retry-after-seconds': '59.244', 'ratelimit-limit': '120', 'ratelimit-remaining': '118',
            'ratelimit-consumed': '2',
            'ratelimit-reset': '2023-08-19T06:13:49.586Z',
            'content-type': 'application/json; charset=utf-8',
            'x-response-time': '1687ms',
            'X-Cloud-Trace-Context': '6b931c8b1b33cce17ee8644b688f97b8',
            'Date': 'Sat, 19 Aug 2023 06:12:51 GMT',
            'Server': 'Google Frontend',
            'Content-Length': '84'
        },
        body={
            'message': 'SUCCESS',
            'id': 1087395,
            'image_id': 'bga',
            'value': None,
            'country_code': 'CN'
        }
    )


@pytest.fixture()
def schema_models():
    return [
        JsonSchemaModel(
            model_name='JsonSchemaModel',
            id='200',
            schema_=JsonTextField(
                text=json.dumps(
                    {
                        "$schema": "http://json-schema.org/draft-07/schema#",
                        "type": "object",
                        "properties": {
                            "message": {
                                "type": "string"
                            },
                            "id": {
                                "type": "integer"
                            },
                            "image_id": {
                                "type": "string"
                            },
                            "value": {
                                "anyOf": [
                                    {
                                        "type": "null"
                                    },
                                    {
                                        "type": "string"
                                    }
                                ],
                            },
                            "country_code": {
                                "type": "string"
                            }
                        },
                        "required": ["message", "id", "image_id", "country_code"]
                    }
                )
            )
        ),
        JsonSchemaModel(
            model_name='JsonSchemaModel',
            id='401',
            schema_=JsonTextField(
                text=json.dumps(
                    {
                        "$schema": "http://json-schema.org/draft-07/schema#",
                        "type": "object",
                        "properties": {
                            "message": {
                                "type": "string",
                                "enum": ["AUTHENTICATION_ERROR"]
                            }
                        },
                        "required": ["message"]
                    }
                )
            )
        ),

    ]


@pytest.fixture()
def schema_validator_model():
    return JsonSchemaValidatorModel(
        model_name='JsonSchemaValidatorModel',
        id='200',
        schema_id='200',
        against='output_body',
    )


def test_schema_validator(
        schema_models,
        json_action_output_model,
        schema_validator_model,
):
    schema_validator = JsonSchemaValidator(
        schema_models=schema_models,
        action_output_model=json_action_output_model,
        schema_validator_model=schema_validator_model
    )
    schema_validator.validate()

    assert schema_validator_model.is_valid and schema_validator_model.exec is None, schema_validator_model.exec
