"""
Scenario Runner

Executes all generated experiment configurations.
"""

class ScenarioRunner:

    def __init__(self, experiment_manager):

        self.experiment_manager = experiment_manager

    ############################################################

    def run(self, configurations):

        results = []

        for configuration in configurations:

            print()

            print("=" * 60)

            print("Running:", configuration.name)

            print(configuration.metadata)

            print("=" * 60)

            result = self.experiment_manager.run(configuration)

            results.append(result)

        return results
