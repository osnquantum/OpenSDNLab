from services.experiment_service import ExperimentService

service = ExperimentService()

network = service.create_experiment(
    name="IPv6 Lab",
    topology="linear",
    hosts=4,
    switches=2,
    protocol="ipv6",
    controller="ryu"
)

network.summary()
