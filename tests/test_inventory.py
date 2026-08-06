from services.experiment_service import ExperimentService
from network.blueprint.network_blueprint import NetworkBlueprint
from network.managers.address_manager import AddressManager
from network.inventory.inventory_manager import InventoryManager

service = ExperimentService()

topology = service.create_experiment(

    name="Inventory Demo",

    topology="linear",

    hosts=4,

    switches=2,

    protocol="dual",

    controller="ryu"

)

blueprint = NetworkBlueprint.from_topology(topology)

AddressManager().assign(

    blueprint,

    protocol="dual"

)

inventory = InventoryManager().build(

    blueprint

)

inventory.summary()

for device in inventory.devices:

    print(device)
