from pathlib import Path
from typing import List, Literal, Dict

import yaml
from pydantic import Field

from api_compose.root.models.specification import SpecificationModel
from api_compose.services.common.models.base import BaseModel


class SessionModel(BaseModel):
    id: str
    description: str = ''

    model_name: Literal['SessionModel'] = Field(
        description=BaseModel.model_fields['model_name'].description
    )

    specifications: List[SpecificationModel]

    @property
    def is_success(self) -> bool:
        return all([spec.is_success for spec in self.specifications])


def parse_session_from_yaml_file(
        file_path: Path,
) -> SessionModel:
    with open(file_path, 'r') as f:
        dict_ = yaml.load(f, Loader=yaml.FullLoader)
        return SessionModel(**dict_)
