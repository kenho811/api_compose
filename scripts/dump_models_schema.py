import json
from typing import List, Dict

from api_compose.services.common.models.base import BaseModel
from api_compose.services.common.registry.processor_registry import ProcessorRegistry


def main():
    models: List[BaseModel] = sum([entry.models for entry in ProcessorRegistry().registry], [])
    for model in models:
        print('============================')
        print(model.model_name)
        schema: Dict = model.model_json_schema()
        print(json.dumps(schema, indent=4))




if __name__ == '__main__':
    main()
