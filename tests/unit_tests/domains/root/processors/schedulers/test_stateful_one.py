from api_compose import SimpleBackend, LocalExecutor
from api_compose.root.processors.schedulers.scheduler import ActionScheduler


def test_scheduler_without_templating(
        start_api_unit_test_server,
        rest_base_url,
        test_run_time_jinja_engine,
        number_stateful_one_scenario,
):
    scheduler = ActionScheduler(
        executor=LocalExecutor(),
        backend=SimpleBackend(),
        jinja_engine=test_run_time_jinja_engine,
        scenario_model=number_stateful_one_scenario,
    )

    scheduler.run()

    post_number_stateful_one_rest_action = number_stateful_one_scenario.actions[0]
    get_number_stateful_one_rest_action = number_stateful_one_scenario.actions[1]
    delete_number_stateful_one_rest_action = number_stateful_one_scenario.actions[2]

    assert post_number_stateful_one_rest_action.output.body == {'message': 'Number is set'}
    assert post_number_stateful_one_rest_action.output.status_code == 200
    assert get_number_stateful_one_rest_action.output.body == {'message': 'Number Available', 'number': 20}
    assert get_number_stateful_one_rest_action.output.status_code == 200
    assert delete_number_stateful_one_rest_action.output.body == {'message': 'Number is deleted'}
    assert delete_number_stateful_one_rest_action.output.status_code == 200
