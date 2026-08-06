from services.experiment_service import ExperimentService

from network.blueprint.network_blueprint import NetworkBlueprint
from network.managers.address_manager import AddressManager
from network.inventory.inventory_manager import InventoryManager

from deployment.deployment_manager import DeploymentManager

############################################################

service = ExperimentService()

topology = service.create_experiment(

    name="Real Deployment",

    topology="linear",

    hosts=2,

    switches=1,

    protocol="ipv4",

    controller="local"

)

############################################################

blueprint = NetworkBlueprint.from_topology(

    topology

)

AddressManager().assign(

    blueprint,

    protocol="ipv4"

)

############################################################

inventory = InventoryManager().build(

    blueprint

)

############################################################

deployment = DeploymentManager()

net = deployment.deploy(
    inventory,
    {
        "type": "remote",
        "name": "osken",
        "ip": "127.0.0.1",
        "port": 6653
    }
)

############################################################

print()

print("Nodes")

print("----------------")

print(net.hosts)

print(net.switches)

print()

print("Running pingAll()")

print("----------------")

net.pingAll()

############################################################

deployment.backend.stop()

print()

print("Deployment finished.")

