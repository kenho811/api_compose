from enum import Enum
from typing import Optional

from pydantic import Field, BaseModel as _BaseModel
from pydantic.json_schema import SkipJsonSchema


class AssertionStateEnum(str, Enum):
    DISCARDED = 'discarded' # Not executed because conditions not met
    EXECUTED = 'executed'
    PENDING = 'pending' # initial state


class JinjaAssertionModel(_BaseModel):
    description: str = Field(description='What this assertion is about')
    template: str

    state: SkipJsonSchema[AssertionStateEnum] = Field(AssertionStateEnum.PENDING, description='State of the Assertion')
    is_success: SkipJsonSchema[bool] = Field(False, description='whether the Assertion item is successful')
    exec: SkipJsonSchema[Optional[str]] = Field(None, description='(If any) Exception raised when test item is executed')
    text: SkipJsonSchema[str] = Field('', description='Text after template is rendered')