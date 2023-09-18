import pytest

from api_compose.root.processors.schedulers.utils import convert_edges_from_str_to_model


@pytest.fixture
def action_models(get_number_stateful_one_rest_action,
                  post_number_stateful_one_rest_action,
                  delete_number_stateful_one_rest_action):
    return [
        get_number_stateful_one_rest_action,
        post_number_stateful_one_rest_action,
        delete_number_stateful_one_rest_action,
    ]


def test_convert_edges_from_str_to_model_linear(
        get_number_stateful_one_rest_action,
        post_number_stateful_one_rest_action,
        delete_number_stateful_one_rest_action,
        action_models,
):
    actual_edges = convert_edges_from_str_to_model(is_schedule_linear=True,
                                                   custom_schedule_order=[],
                                                   action_models=action_models)

    expected_edges = [
        (get_number_stateful_one_rest_action, post_number_stateful_one_rest_action),
        (post_number_stateful_one_rest_action, delete_number_stateful_one_rest_action)
    ]

    assert actual_edges == expected_edges


def test_convert_edges_from_str_to_model_custom(
        get_number_stateful_one_rest_action,
        post_number_stateful_one_rest_action,
        action_models,
):
    actual_edges = convert_edges_from_str_to_model(is_schedule_linear=False,
                                                   custom_schedule_order=[
                                       (get_number_stateful_one_rest_action.execution_id,
                                        post_number_stateful_one_rest_action.execution_id),
                                   ],
                                                   action_models=action_models)

    expected_edges = [
        (get_number_stateful_one_rest_action, post_number_stateful_one_rest_action),
    ]

    assert actual_edges == expected_edges
