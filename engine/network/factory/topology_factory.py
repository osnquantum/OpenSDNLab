"""
OpenSDNLab Topology Factory

Creates topology objects using registered builders.
"""

from engine.network.builders import LinearBuilder
from engine.network.builders.custom_builder import CustomBuilder

from engine.core.logger import logger


class TopologyFactory:

    def __init__(self):

        self.builders = {

            "linear": LinearBuilder(),
            "custom": CustomBuilder(),

        }

    ####################################################################

    def create(
        self,
        topology="linear",
        hosts=2,
        switches=1,
        protocol="ipv6",
        controller="ryu",
        name="Experiment",
        topology_data=None
    ):

        logger.info(f"Creating topology: {topology}")

        builder = self.builders.get(
            topology.lower()
        )

        if builder is None:

            raise ValueError(
                f"Unsupported topology: {topology}"
            )

        if topology.lower() == "custom":

            network = builder.build(
                topology_data or {},
                protocol,
                controller,
                name
            )

        else:

            network = builder.build(
                hosts,
                switches,
                protocol,
                controller,
                name
            )

        logger.info("Topology created successfully.")

        return network
