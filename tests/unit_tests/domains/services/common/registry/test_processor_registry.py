import pytest

from api_compose.services.common.exceptions import ModelNotFoundException, ProcessorNotFoundException, \
    ProcessorNonUniqueException
from api_compose.services.common.processors.base import BaseProcessor
from api_compose.services.common.registry.processor_registry import ProcessorRegistry, ProcessorCategory



def test_raise_model_not_found():
    with pytest.raises(ModelNotFoundException):
        ProcessorRegistry.create_model_by_model_name(
            model_name='NonExistentDoSomethingModel',
            config={}
        )


def test_raise_processor_not_found():
    with pytest.raises(ProcessorNotFoundException):
        ProcessorRegistry.create_processor_by_name(
            class_name='NonExistentDoSomething',
            config={}
        )


def test_raise_processor_registered_twice():
    backup = [entry for entry in ProcessorRegistry.registry]
    ProcessorRegistry.registry = []
    with pytest.raises(ProcessorNonUniqueException):
        @ProcessorRegistry.set(
            models=[],
            processor_category=ProcessorCategory._Unknown,
        )
        class DuplicateProcessor(BaseProcessor):
            def do_something(self):
                print('do something')

        @ProcessorRegistry.set(
            models=[],
            processor_category=ProcessorCategory._Unknown,
        )
        class DuplicateProcessor(BaseProcessor):
            def do_some_other_thing(self):
                print('do something')

    ProcessorRegistry.registry = backup


def test_can_register_class_and_create_processor_by_name(
        number_one_processor,
):
    # Lookup the class by annotation
    assert type(ProcessorRegistry.create_processor_by_name('NumberOneProcessor', config={})) == number_one_processor


def test_can_register_class_and_create_model_by_name(
        number_one_model_config,
        number_one_model_class,
        number_one_processor,
):
    # Lookup the class by annotation
    assert type(ProcessorRegistry.create_model_by_model_name('NumberOneModel', number_one_model_config)) == number_one_model_class
