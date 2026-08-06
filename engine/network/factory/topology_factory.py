"""
OpenSDNLab Topology Factory

Creates topology objects using registered builders.
"""

from engine.network.builders import LinearBuilder

from engine.core.logger import logger


class TopologyFactory:

    def __init__(self):

        self.builders = {

            "linear": LinearBuilder(),

        }

    ####################################################################

    def create(
        self,
        topology="linear",
        hosts=2,
        switches=1,
        protocol="ipv6",
        controller="ryu",
        name="Experiment"
    ):

        logger.info(f"Creating topology: {topology}")

        builder = self.builders.get(topology)

        if builder is None:

            raise ValueError(
                f"Unsupported topology: {topology}"
            )

        network = builder.build(
            hosts,
            switches,
            protocol,
            controller,
            name
        )

        logger.info("Topology created successfully.")

        return network
