from models.experiment_configuration import ExperimentConfiguration

config = ExperimentConfiguration(
    name="Configuration Demo"
)

print()

print(config)

print()

print(config.topology)

print(config.network)

print(config.controller)

print(config.deployment)
