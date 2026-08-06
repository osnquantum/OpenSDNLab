"""
Experiment Manager

Coordinates the complete experiment lifecycle.
"""

from services.experiment_service import ExperimentService

from network.blueprint.network_blueprint import NetworkBlueprint
from network.managers.address_manager import AddressManager
from network.inventory.inventory_manager import InventoryManager

from deployment.deployment_manager import DeploymentManager

from monitoring.monitoring_manager import MonitoringManager

from repository.experiment_repository import ExperimentRepository
from repository.models import ExperimentResult

class ExperimentManager:

    def __init__(self):

        self.experiment_service = ExperimentService()

        self.address_manager = AddressManager()

        self.inventory_manager = InventoryManager()

        self.deployment_manager = DeploymentManager()

        self.monitoring_manager = MonitoringManager()

        self.repository = ExperimentRepository()

    ############################################################

    def build_experiment(
        self,
        name,
        topology,
        hosts,
        switches,
        protocol,
        controller
    ):

        network = self.experiment_service.create_experiment(
            name=name,
            topology=topology,
            hosts=hosts,
            switches=switches,
            protocol=protocol,
            controller=controller
        )

        blueprint = NetworkBlueprint.from_topology(
            network
        )

        self.address_manager.assign(
            blueprint,
            protocol=protocol
        )

        inventory = self.inventory_manager.build(
            blueprint
        )

        return inventory
