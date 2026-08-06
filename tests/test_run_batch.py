from services.experiment_manager import ExperimentManager

manager = ExperimentManager()

print()

print("run_batch available:", hasattr(manager, "run_batch"))
