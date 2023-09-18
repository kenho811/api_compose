import time

from api_compose.services.common.models.text_field.templated_text_field import IntegerTemplatedTextField
from api_compose.services.composition_service.jinja.context import ActionJinjaContext
from api_compose.services.composition_service.models.actions.actions.dummy_action import DummyActionModel
from api_compose.services.composition_service.models.actions.configs.dummy_configs import DummyActionConfigModel
from api_compose.services.composition_service.processors.adapters.dummy_adapter import DummyAdapter


def test_dummy_adapter_can_sleep(
        test_run_time_jinja_engine,
):
    model = DummyActionModel(
        id='sleep_action',
        config=DummyActionConfigModel(
            sleep_seconds=IntegerTemplatedTextField(template='2')
        )
    )

    adapter = DummyAdapter(
        action_model=model,
        jinja_engine=test_run_time_jinja_engine,
    )
    adapter.start(jinja_context=ActionJinjaContext(current_action_model=model))
    adapter.stop()

    assert model.input.sleep_seconds == 2




