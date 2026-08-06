"""
Scenario Variable
"""

from dataclasses import dataclass


@dataclass
class ScenarioVariable:

    name: str

    values: list
