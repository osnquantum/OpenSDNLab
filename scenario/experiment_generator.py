"""
Scenario Experiment Generator
"""

from copy import deepcopy


class ExperimentGenerator:

    def generate(self, base_configuration, experiments):

        generated = []

        for experiment in experiments:

            config = deepcopy(base_configuration)

            for key, value in experiment.items():

                if key in config.deployment:

                    config.deployment[key] = value

                elif key in config.network:

                    config.network[key] = value

                elif key in config.controller:

                    config.controller[key] = value

                elif key in config.topology:

                    config.topology[key] = value

                else:

                    config.metadata[key] = value

            generated.append(config)

        return generated
