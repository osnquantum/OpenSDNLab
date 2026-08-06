"""
Scenario
"""

from dataclasses import dataclass, field

from engine.scenario.scenario_variable import ScenarioVariable


@dataclass
class Scenario:

    name: str

    variables: list[ScenarioVariable] = field(default_factory=list)
