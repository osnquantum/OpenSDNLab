from services.experiment_service import ExperimentService

from network.blueprint.network_blueprint import NetworkBlueprint

from network.managers.address_manager import AddressManager

service = ExperimentService()

topology = service.create_experiment(

    name="IPv6 Lab",

    topology="linear",

    hosts=5,

    switches=2,

    protocol="dual",

    controller="ryu"

)

blueprint = NetworkBlueprint.from_topology(topology)

manager = AddressManager()

manager.assign(

    blueprint,

    protocol="dual",

    ipv4_prefix="10.0.0.0/24",

    ipv6_prefix="2001:D30:1212:A123::/64"

)

print()

for host in blueprint.hosts:

    print(

        host.name,

        host.ipv4,

        host.ipv6,

        host.mac

    )
