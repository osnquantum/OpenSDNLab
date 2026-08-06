from services.experiment_manager import ExperimentManager

manager = ExperimentManager()

inventory = manager.build_experiment(
    name="Deployment Demo",
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
print("Deployment Successful")
print("---------------------")
print(net)

manager.deployment_manager.backend.stop()
