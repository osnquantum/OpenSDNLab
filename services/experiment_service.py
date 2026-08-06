"""
OpenSDNLab Experiment Service

Coordinates the complete experiment lifecycle.
"""

from core.logger import logger
from network.factory.topology_factory import TopologyFactory


class ExperimentService:

    def __init__(self):

        self.factory = TopologyFactory()

    ##################################################################

    def create_experiment(
        self,
        name,
        topology,
        hosts,
        switches,
        protocol,
        controller
    ):

        logger.info(f"Creating experiment: {name}")

        network = self.factory.create(
            topology=topology,
            hosts=hosts,
            switches=switches,
            protocol=protocol,
            controller=controller,
            name=name
        )

        logger.info("Experiment created successfully.")

        return network
