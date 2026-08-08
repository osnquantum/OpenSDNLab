"""
Linear Topology Builder
"""

from engine.network.models import Topology
from engine.network.models import Host
from engine.network.models import Switch
from engine.network.models import Link

from engine.network.builders.base_builder import BaseBuilder


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

                Host(
                    name=f"h{i}",
                    ipv4=f"10.0.0.{i}/24",
                    ipv6=f"2001:db8::{i}",
                    mac=f"00:00:00:00:00:{i:02x}"
                )

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
