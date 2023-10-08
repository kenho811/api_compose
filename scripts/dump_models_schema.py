from typing import List

from api_compose.services.common.models.base import BaseModel
from api_compose.services.common.registry.processor_registry import ProcessorRegistry


def main():
    models: List[BaseModel] = sum([entry.models for entry in ProcessorRegistry().registry], [])
    for model in models:
        print(model.model_dump_json(indent=4))


if __name__ == '__main__':
    main()
