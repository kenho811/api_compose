from typing import Literal

import pytest
from pydantic import Field

from api_compose.services.common.models.base import BaseModel
from api_compose.services.common.processors.base import BaseProcessor
from api_compose.services.common.registry.processor_registry import ProcessorRegistry, ProcessorCategory


@pytest.fixture
def number_one_model_class():
    class NumberOneModel(BaseModel):
        model_name: Literal['NumberOneModel'] = Field(
            description=BaseModel.model_fields['model_name'].description
        )


    return NumberOneModel


@pytest.fixture
def number_one_model_config():
    return dict(
        id='number_one_model',
        model_name='NumberOneModel',

        description='"Do something"'
    )

@pytest.fixture
def number_one_model(
        number_one_model_class,
        number_one_model_config
):
    return number_one_model_class(**number_one_model_config)

@pytest.fixture()
def number_one_processor(
        number_one_model,
):
    backup = [entry for entry in ProcessorRegistry.registry]
    ProcessorRegistry.registry = []
    @ProcessorRegistry.set(
        processor_category=ProcessorCategory._Unknown,
        models=[
            number_one_model,
        ]
    )
    class NumberOneProcessor(BaseProcessor):
        pass

    yield NumberOneProcessor

    ProcessorRegistry.registry = backup

