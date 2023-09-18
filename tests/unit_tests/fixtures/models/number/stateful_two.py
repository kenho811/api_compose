import pytest

from api_compose.root.models.schedulers.configs import ActionSchedulerConfigModel
from api_compose.services.assertion_service.models.jinja_assertion import JinjaAssertionModel

from api_compose.root.models.scenario import ScenarioModel, ScenarioModelConfig
from api_compose.services.common.models.text_field.templated_text_field import StringTemplatedTextField, JsonTemplatedTextField
from api_compose.services.common.models.text_field.text_field import TextFieldFormatEnum
from api_compose.services.composition_service.models.actions.actions.http_actions import JsonHttpActionModel
from api_compose.services.composition_service.models.actions.configs.http_configs import JsonHttpActionConfigModel
from api_compose.services.composition_service.models.executors.configs import LocalExecutorConfigModel
from api_compose.services.composition_service.models.executors.enum import ExecutorProcessorEnum


@pytest.fixture()
def number_stateful_two_scenario(
        get_number_stateful_two_rest_action,
        post_number_stateful_two_rest_action
) -> ScenarioModel:
    return ScenarioModel(model_name='ScenarioModel',
        id='scenario_three',
        description='Test can get and post the correct number',
        config=ScenarioModelConfig(
            executor=ExecutorProcessorEnum.LocalExecutor,
            executor_config=LocalExecutorConfigModel(),
            scheduler_config=ActionSchedulerConfigModel(
                max_concurrent_node_execution_num=5,
                rescan_all_nodes_in_seconds=1,
                is_schedule_linear=True,
                custom_schedule_order=[]
            )
        ),

        actions=[
            get_number_stateful_two_rest_action,
            post_number_stateful_two_rest_action,
        ],
        assertion_items=[
            JinjaAssertionModel(
                description='Assert Guess is correct',
                template="{{ action('post_number_stateful_two')| output_body| jpath('$.message') == 'Your guess is correct!' }}",
            ),
            JinjaAssertionModel(
                description='Assert Status Code is 200',
                template="{{ action('post_number_stateful_two') | output_status_code == 200 }}"
            )
        ],
    )


@pytest.fixture()
def get_number_stateful_two_rest_action(rest_base_url) -> JsonHttpActionModel:
    """
    Get number from server
    """
    return JsonHttpActionModel(model_name='JsonHttpActionModel',
        id='get_number_stateful_two',
        parent_ids=['test_suite_one', 'scenario_three'],
        description='Get Number Stateful',
        execution_id='get_number_stateful_two',
        config=JsonHttpActionConfigModel(
            url=StringTemplatedTextField(template=rest_base_url + '/unit/number/stateful-two',
                                         format=TextFieldFormatEnum.STRING),
            method=StringTemplatedTextField(template='GET', format=TextFieldFormatEnum.STRING),
            headers=JsonTemplatedTextField(template='{}', format=TextFieldFormatEnum.JSON),
            params=JsonTemplatedTextField(template='{}', format=TextFieldFormatEnum.JSON),
            body=JsonTemplatedTextField(template='{}', format=TextFieldFormatEnum.JSON),
        ),
    )


@pytest.fixture()
def post_number_stateful_two_rest_action(rest_base_url) -> JsonHttpActionModel:
    """
    Post number to server
    """
    return JsonHttpActionModel(model_name='JsonHttpActionModel',
        id='post_number_stateful_two',
        parent_ids=['test_suite_one', 'scenario_three'],
        description='Post Number Stateful',
        execution_id='post_number_stateful_two',
        config=JsonHttpActionConfigModel(
            url=StringTemplatedTextField(template=rest_base_url + '/unit/number/stateful-two',
                                         format=TextFieldFormatEnum.STRING),
            method=StringTemplatedTextField(template='POST', format=TextFieldFormatEnum.STRING),
            headers=JsonTemplatedTextField(template='{}', format=TextFieldFormatEnum.JSON),
            params=JsonTemplatedTextField(template='{}', format=TextFieldFormatEnum.JSON),
            body=JsonTemplatedTextField(
                template="""
                    {"number": {{ action('get_number_stateful_two') | output_body| jpath('$.number') }} }
                """,
                format=TextFieldFormatEnum.JSON, )
        ),
    )
