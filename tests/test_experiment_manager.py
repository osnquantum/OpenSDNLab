from services.experiment_manager import ExperimentManager

manager = ExperimentManager()

inventory = manager.build_experiment(
    name="Manager Demo",
    topology="linear",
    hosts=2,
    switches=1,
    protocol="ipv4",
    controller="osken"
)

print()
print("Inventory")
print("----------------")
print(inventory)
