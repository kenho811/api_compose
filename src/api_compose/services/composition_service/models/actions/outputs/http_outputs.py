import warnings as w
from typing import Dict, Union, List

from api_compose.core.logging import get_logger
from api_compose.core.lxml.parser import PrintableElementAnnotation, get_default_element
from api_compose.services.composition_service.events.action import ActionEvent

w.filterwarnings('ignore', module='pydantic')  # Warning of lxml.etree.E.default() as default in model

from pydantic import Field, ConfigDict, field_validator

from api_compose.services.composition_service.models.actions.outputs.base_outputs import BaseActionOutputModel

logger = get_logger(__name__)


class BaseHttpActionOutputModel(BaseActionOutputModel):
    url: str = Field(
        "",
        description="URL",
    )
    headers: Dict = Field(
        {},
        description="headers",
    )


class JsonHttpActionOutputModel(BaseHttpActionOutputModel):
    body: Union[List, Dict] = Field(
        {},
        description="body",
    )

    @field_validator('body')
    @classmethod
    def validate_body(cls, values):
        if type(values) not in [list, dict]:
            logger.error(f'Body {values} (type: {type(values)} is neither a list nor dict', ActionEvent)
            return {}
        else:
            return values


class XmlHttpActionOutputModel(BaseHttpActionOutputModel):
    # FIXME
    model_config = ConfigDict(arbitrary_types_allowed=True)

    body: PrintableElementAnnotation = Field(
        get_default_element(),
        description="body",
    )


w.filterwarnings('default')  # Reset
