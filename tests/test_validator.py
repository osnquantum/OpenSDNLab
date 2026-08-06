from services.experiment_service import ExperimentService
from network.blueprint.network_blueprint import NetworkBlueprint
from network.managers.address_manager import AddressManager
from network.validators.blueprint_validator import BlueprintValidator

service = ExperimentService()

topology = service.create_experiment(

    name="Validation Demo",

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

BlueprintValidator().validate(blueprint)

print()

print("Blueprint validation successful.")

