"""
Experiment Pipeline

End-to-end orchestration of an SDN experiment.
"""

from engine.core.logger import logger

from engine.services.experiment_service import ExperimentService

from engine.network.blueprint.network_blueprint import NetworkBlueprint
from engine.network.managers.address_manager import AddressManager
from engine.network.validators.blueprint_validator import BlueprintValidator
from engine.network.inventory.inventory_manager import InventoryManager

from engine.deployment.deployment_manager import DeploymentManager


class ExperimentPipeline:

    def __init__(self):

        self.service = ExperimentService()

        self.address_manager = AddressManager()

        self.validator = BlueprintValidator()

        self.inventory_manager = InventoryManager()

        self.deployment_manager = DeploymentManager()

    ############################################################

    def run(self, config):

        logger.info("========== Experiment Pipeline ==========")

        ########################################################
        # Create Topology
        ########################################################

        topology = self.service.create_experiment(config)

        ########################################################
        # Blueprint
        ########################################################

        blueprint = NetworkBlueprint.from_topology(topology)

        ########################################################
        # Address Assignment
        ########################################################

        protocol = config.network.get("protocol", "ipv4")

        self.address_manager.assign(
            blueprint,
            protocol=protocol
        )

        ########################################################
        # Validation
        ########################################################

        self.validator.validate(blueprint)

        ########################################################
        # Inventory
        ########################################################

        inventory = self.inventory_manager.build(
            blueprint
        )

        ########################################################
        # Deployment
        ########################################################

        self.deployment_manager.deploy(
            inventory
        )

        logger.info("Pipeline completed successfully")

        return inventory

