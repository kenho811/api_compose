import time

from api_compose.core.jinja.core.engine import JinjaEngine
from api_compose.core.logging import get_logger
from api_compose.core.settings.settings import GlobalSettingsModelSingleton
from api_compose.root.events import ScenarioEvent
from api_compose.root.models.scenario import ScenarioModel
from api_compose.root.processors.schedulers.scheduler import ActionScheduler
from api_compose.services.assertion_service.events import AssertionEvent
from api_compose.services.assertion_service.models.jinja_assertion import AssertionStateEnum
from api_compose.services.assertion_service.processors.i_jinja_assertion import InteractiveJinjaAssertion
from api_compose.services.assertion_service.processors.jinja_assertion import JinjaAssertion
from api_compose.services.common.processors.base import BaseProcessor
from api_compose.services.common.registry.processor_registry import ProcessorRegistry, ProcessorCategory
from api_compose.services.composition_service.jinja.context import ActionJinjaContext
from api_compose.services.composition_service.models.actions.states import ActionStateEnum
from api_compose.services.composition_service.processors.executors.base_executor import BaseExecutor
from api_compose.services.persistence_service.processors.base_backend import BaseBackend

logger = get_logger(__name__)


@ProcessorRegistry.set(

    processor_category=ProcessorCategory.Backend,
    models=[
        ScenarioModel(
            model_name='ScenarioModel',
            id='example_scenario',
            description='example scenario',
            actions=[],
        )
    ]
)
class ScenarioProcessor(BaseProcessor):

    def __init__(self,
                 scenario_model: ScenarioModel,
                 backend: BaseBackend,
                 jinja_engine: JinjaEngine,
                 ):
        super().__init__()
        self.scenario_model = scenario_model
        self.jinja_engine = jinja_engine
        self.backend = backend

        self.executor: BaseExecutor = ProcessorRegistry.create_processor_by_name(
            class_name=scenario_model.config.executor.value,
            config=dict(scenario_model.config.executor_config),
        )

        self.action_scheduler: ActionScheduler = ActionScheduler(
            backend=backend,
            jinja_engine=jinja_engine,
            executor=self.executor,
            scenario_model=scenario_model,
        )

    def run(self):
        logger.info(f' Scenario started - {self.scenario_model.fqn}', ScenarioEvent())
        # Run Actions
        self.scenario_model.start_time = time.time()
        self.action_scheduler.run()
        self.scenario_model.end_time = time.time()
        logger.info(f' Scenario ended - {self.scenario_model.fqn}', ScenarioEvent())

        # Get ActionJinjaContext
        jinja_context = ActionJinjaContext.build(
            backend=self.backend,
            action_model=self.scenario_model.actions[0],
            append_current_action_model=False,
        )

        # Skip Assertions if not all actions are in ENDED state
        logger.info(f'Assertions for scenario started - {self.scenario_model.fqn}', AssertionEvent())
        is_all_actions_ended = all(action.state == ActionStateEnum.ENDED for action in self.scenario_model.actions)

        if is_all_actions_ended:
            if GlobalSettingsModelSingleton.get().cli_options.is_interactive:
                # Dynamic Jinja Template Generation
                if len(self.scenario_model.assertions) > 0:
                    logger.warning(
                        f'Pre-defined Assertions for Scenario {self.scenario_model.id} will be overwritten',
                        AssertionEvent()
                    )
                    self.scenario_model.assertions = []

                logger.info(
                    f"Dropping to an interactive Jinja Session for Scenario {self.scenario_model.id=}",
                    AssertionEvent()
                )
                # Jinja Template is generated dynamically
                i_jinja_assertion = InteractiveJinjaAssertion(
                    jinja_engine=self.jinja_engine,
                    jinja_context=jinja_context,
                )
                i_jinja_assertion.cmdloop()
                self.scenario_model.assertions = i_jinja_assertion.assertions
            else:
                # Jinja Template is pre-defined
                for assertion_model in self.scenario_model.assertions:
                    jinja_assertion = JinjaAssertion(
                        assertion_model=assertion_model,
                        jinja_engine=self.jinja_engine,
                        jinja_context=jinja_context,
                    )
                    jinja_assertion.run()
        else:
            logger.error(
                f'Discarding Assertions for scenario {self.scenario_model.fqn} as not all actions are in {ActionStateEnum.ENDED}',
                AssertionEvent()
            )
            for assertion_model in self.scenario_model.assertions:
                assertion_model.state = AssertionStateEnum.DISCARDED
        logger.info(
            f'Assertions for scenario ended - {self.scenario_model.fqn} as not all actions are in {ActionStateEnum.ENDED}',
            AssertionEvent()
        )

        # Save results
        self.backend.add(self.scenario_model)
