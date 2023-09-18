from api_compose import SimpleBackend, LocalExecutor
from api_compose.root.processors.schedulers.scheduler import ActionScheduler


def test_scheduler_with_templating(
        rest_server,
        test_run_time_jinja_engine,
        number_stateful_two_scenario,
):

    scheduler = ActionScheduler(
        executor=LocalExecutor(),
        backend=SimpleBackend(),
        jinja_engine=test_run_time_jinja_engine,
        scenario_model=number_stateful_two_scenario,
    )

    scheduler.run()

    get_number_stateful_two_rest_action = number_stateful_two_scenario.actions[0]
    post_number_stateful_two_rest_action = number_stateful_two_scenario.actions[1]

    assert get_number_stateful_two_rest_action.output.status_code == 200
    assert post_number_stateful_two_rest_action.output.status_code == 200
    assert post_number_stateful_two_rest_action.output.body == {'message': f'Your guess is correct!'}
