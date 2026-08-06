"""
Linear Topology Builder
"""

from network.models import Topology
from network.models import Host
from network.models import Switch
from network.models import Link

from network.builders.base_builder import BaseBuilder


class LinearBuilder(BaseBuilder):

    def build(
        self,
        hosts,
        switches,
        protocol,
        controller,
        name
    ):

        topology = Topology(
            name=name,
            topology_type="linear",
            protocol=protocol,
            controller=controller
        )

        for i in range(1, switches + 1):
            topology.switches.append(
                Switch(f"s{i}")
            )

        for i in range(1, hosts + 1):
            topology.hosts.append(
                Host(f"h{i}")
            )

        for i in range(hosts):

            sw = min(i, switches - 1)

            topology.links.append(
                Link(
                    topology.hosts[i].name,
                    topology.switches[sw].name
                )
            )

        for i in range(switches - 1):

            topology.links.append(
                Link(
                    topology.switches[i].name,
                    topology.switches[i + 1].name
                )
            )

        return topology
