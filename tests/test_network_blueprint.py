from services.experiment_service import ExperimentService

from network.blueprint.network_blueprint import NetworkBlueprint

service = ExperimentService()

topology = service.create_experiment(

    name="IPv6 SDN Experiment",

    topology="linear",

    hosts=4,

    switches=2,

    protocol="ipv6",

    controller="ryu"

)

blueprint = NetworkBlueprint.from_topology(topology)

blueprint.summary()

blueprint.export_json("experiments/ipv6_sdn.json")

print("Blueprint exported successfully.")
