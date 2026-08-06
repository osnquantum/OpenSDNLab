from models.experiment_configuration import ExperimentConfiguration

from scenario.scenario import Scenario
from scenario.scenario_variable import ScenarioVariable
from scenario.scenario_engine import ScenarioEngine
from scenario.experiment_generator import ExperimentGenerator

base = ExperimentConfiguration(
    name="Delay Analysis"
)

scenario = Scenario(
    name="Delay Study"
)

scenario.variables.append(
    ScenarioVariable(
        "delay",
        [
            "1ms",
            "5ms",
            "10ms"
        ]
    )
)

engine = ScenarioEngine()

experiments = engine.generate(scenario)

generator = ExperimentGenerator()

configs = generator.generate(
    base,
    experiments
)

print()

for config in configs:

    print(
        config.deployment["delay"]
    )
