from pprint import pprint

from services.experiment_service import ExperimentService
from network.blueprint.network_blueprint import NetworkBlueprint
from network.managers.address_manager import AddressManager
from deployment.adapters.blueprint_adapter import BlueprintAdapter


service = ExperimentService()

topology = service.create_experiment(

    name="Blueprint Adapter Demo",

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

adapter = BlueprintAdapter()

plan = adapter.convert(blueprint)

print()

print("========== DEPLOYMENT PLAN ==========")

pprint(plan)

print("=====================================")
