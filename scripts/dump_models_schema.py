import json
from typing import List, Dict, Type

from api_compose.services.common.models.base import BaseModel
from api_compose.services.common.registry.processor_registry import ProcessorRegistry
from api_compose.services.composition_service.models.actions.actions.http_actions import JsonHttpActionModel

model_to_fields_mapping: Dict[Type[BaseModel], List[str]] = {
    JsonHttpActionModel: ['model_name'],
}


def main():
    for model, attrs in model_to_fields_mapping.items():
        model.model_json_schema(inclu)
    models: List[BaseModel] = sum([entry.models for entry in ProcessorRegistry().registry], [])
    for model in models:
        print('============================')
        print(model.model_name)
        schema: Dict = model.model_json_schema()
        print(json.dumps(schema, indent=4))


if __name__ == '__main__':
    main()
