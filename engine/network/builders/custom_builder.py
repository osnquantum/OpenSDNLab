"""
Custom Topology Builder

Builds a Topology from the topology designer JSON.
"""

from engine.network.models import Topology
from engine.network.models import Host
from engine.network.models import Switch
from engine.network.models import Link

from engine.network.builders.base_builder import BaseBuilder


class CustomBuilder(BaseBuilder):

    def build(
        self,
        topology_data,
        protocol,
        controller,
        name
    ):

        topology = Topology(
            name=name,
            topology_type="custom",
            protocol=protocol,
            controller=controller
        )

        nodes = topology_data.get(
            "nodes",
            []
        )

        links = topology_data.get(
            "links",
            []
        )

        # ----------------------------------------------------
        # Hosts
        # ----------------------------------------------------

        host_number = 1

        for node in nodes:

            if node.get("type") != "host":
                continue

            host_name = node.get(
                "id",
                f"h{host_number}"
            )

            topology.hosts.append(
                Host(
                    name=host_name,
                    ipv4=f"10.0.0.{host_number}/24",
                    ipv6=f"2001:db8::{host_number}",
                    mac=f"00:00:00:00:00:{host_number:02x}"
                )
            )

            host_number += 1

        # ----------------------------------------------------
        # Switches
        # ----------------------------------------------------

        for node in nodes:

            if node.get("type") != "switch":
                continue

            switch_name = node.get("id")

            topology.switches.append(
                Switch(
                    name=switch_name
                )
            )

        # ----------------------------------------------------
        # Links
        # ----------------------------------------------------

        for item in links:

            source = item.get(
                "source"
            )

            target = item.get(
                "target",
                item.get("destination")
            )

            if not source or not target:
                continue

            topology.links.append(
                Link(
                    source=source,
                    destination=target,
                    source_port=item.get(
                        "source_port"
                    ),
                    destination_port=item.get(
                        "destination_port"
                    )
                )
            )

        return topology
