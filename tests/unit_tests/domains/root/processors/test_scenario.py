from api_compose.root.processors.scenario import ScenarioProcessor
from api_compose.services.persistence_service.processors.simple_backend import SimpleBackend


def test_scenario(
        start_rest_server,
        number_stateful_two_scenario,
        test_run_time_jinja_engine,
):
    processor = ScenarioProcessor(
        scenario_model=number_stateful_two_scenario,
        backend=SimpleBackend(),
        jinja_engine=test_run_time_jinja_engine,
    )

    processor.run()

    assert number_stateful_two_scenario.is_success
