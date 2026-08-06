"""
Increasing Delay Scenario
"""

from scenario.scenario import Scenario
from scenario.scenario_variable import ScenarioVariable


def create():

    scenario = Scenario(

        name="Increasing Delay"

    )

    scenario.variables.append(

        ScenarioVariable(

            "delay",

            [

                "1ms",

                "5ms",

                "10ms",

                "20ms",

                "50ms"

            ]

        )

    )

    return scenario
