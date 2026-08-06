from services.experiment_manager import ExperimentManager

manager = ExperimentManager()

inventory = manager.build_experiment(
    name="Monitoring Demo",
    topology="linear",
    hosts=2,
    switches=1,
    protocol="ipv4",
    controller="osken"
)

net = manager.deploy_experiment(
    inventory,
    {
        "type": "remote",
        "name": "osken",
        "ip": "127.0.0.1",
        "port": 6653
    }
)

print()

print("Running Monitoring")

print("------------------")

report = manager.monitor_experiment(
    net
)

print(report)

manager.deployment_manager.backend.stop()
