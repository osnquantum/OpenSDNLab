from services.experiment_manager import ExperimentManager

manager = ExperimentManager()

result = manager.run(
    name="Complete Experiment",
    topology="linear",
    hosts=2,
    switches=1,
    protocol="ipv4",
    controller_config={
        "type":"remote",
        "name":"osken",
        "ip":"127.0.0.1",
        "port":6653
    }
)

print()
print("Experiment Completed")
print("--------------------")
print(result)
