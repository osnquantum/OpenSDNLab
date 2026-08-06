"""
Scenario Engine
"""

from itertools import product


class ScenarioEngine:

    def generate(self, scenario):

        names = [v.name for v in scenario.variables]

        values = [v.values for v in scenario.variables]

        experiments = []

        for combination in product(*values):

            experiments.append(

                dict(zip(names, combination))

            )

        return experiments
