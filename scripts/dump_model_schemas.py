import json
import sys
from pathlib import Path
from typing import List, Dict

from api_compose.services.common.models.base import BaseModel
from api_compose.services.common.registry.processor_registry import ProcessorRegistry


def main(output_folder_path: Path):
    models: List[BaseModel] = sum([entry.models for entry in ProcessorRegistry().registry], [])
    for model in models:
        print('============================')
        file_path = output_folder_path.joinpath(model.model_name)
        schema: Dict = model.model_json_schema()
        with open(file_path, 'w') as schema_file:
            schema_str: str = json.dumps(schema, indent=4)
            print(f'dumping below schema to path {file_path.absolute()}')
            print(schema_str)
            schema_file.write(json.dumps(schema, indent=4))


if __name__ == '__main__':
    if len(sys.argv) == 2:
        output_folder_path = sys.argv[1]
        output_folder_path = Path(output_folder_path)
        output_folder_path.mkdir(parents=True, exist_ok=True)
        main(output_folder_path)
    else:
        raise ValueError('Usage: python dump_model_schemas.py {output_folder_path}')
