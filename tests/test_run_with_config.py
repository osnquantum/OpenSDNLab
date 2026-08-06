from models.experiment_configuration import ExperimentConfiguration
from services.experiment_manager import ExperimentManager

config = ExperimentConfiguration(
    name="Configuration Experiment"
)

manager = ExperimentManager()

result = manager.run(config)

print()

print("Experiment Completed")

print("--------------------")

print(result)
