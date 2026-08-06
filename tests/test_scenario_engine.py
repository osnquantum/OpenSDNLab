from scenario.scenario import Scenario
from scenario.scenario_variable import ScenarioVariable
from scenario.scenario_engine import ScenarioEngine


scenario = Scenario(

    name="Delay Comparison"

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

experiments = engine.generate(

    scenario

)

print()

for experiment in experiments:

    print(experiment)
