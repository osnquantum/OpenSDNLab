"""
Topology Integrity Validator

Ensures that all declared hosts and switches participate
in a valid network topology before Mininet deployment.
"""


class TopologyIntegrityValidator:

    def validate(self, blueprint):

        nodes = set()

        for host in blueprint.hosts:
            nodes.add(host.name)

        for switch in blueprint.switches:
            nodes.add(switch.name)

        connected_nodes = set()

        for link in blueprint.links:

            source = link.source
            destination = link.destination

            if source not in nodes:
                raise ValueError(
                    f"Topology link references unknown node: {source}"
                )

            if destination not in nodes:
                raise ValueError(
                    f"Topology link references unknown node: {destination}"
                )

            connected_nodes.add(source)
            connected_nodes.add(destination)

        disconnected = nodes - connected_nodes

        if disconnected:

            raise ValueError(
                "Topology contains disconnected node(s): "
                + ", ".join(sorted(disconnected))
            )

        return {
            "valid": True,
            "nodes": len(nodes),
            "links": len(blueprint.links),
            "connected_nodes": len(connected_nodes),
        }
