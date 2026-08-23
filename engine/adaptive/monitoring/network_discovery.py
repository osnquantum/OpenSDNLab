"""
Network Discovery

Builds a unified network representation from either:

1. OpenSDNLab static Inventory
2. Live OS-Ken discovered topology

The output provides hosts, switches, links, a graph,
and complete reachability information.
"""


class NetworkDiscovery:

    def discover(self, inventory):

        hosts = []
        switches = []
        links = []

        for device in inventory.devices:

            if device.device_type == "host":
                hosts.append(device.hostname)

            elif device.device_type == "switch":
                switches.append(device.hostname)

        for link in inventory.links:

            source = link.source
            destination = link.destination

            link_id = "-".join(
                sorted([source, destination])
            )

            links.append({
                "id": link_id,
                "source": source,
                "destination": destination,
                "bandwidth": getattr(
                    link,
                    "bandwidth",
                    None
                ),
                "delay": getattr(
                    link,
                    "delay",
                    None
                ),
                "loss": getattr(
                    link,
                    "loss",
                    None
                )
            })

        graph = self._build_graph(
            switches=switches,
            links=links,
        )

        reachability = self._build_reachability(
            graph
        )

        return {
            "hosts": hosts,
            "switches": switches,
            "links": links,
            "graph": graph,
            "reachability": reachability,
            "device_count": len(
                inventory.devices
            ),
            "host_count": len(hosts),
            "switch_count": len(switches),
            "link_count": len(links),
        }


    def discover_live(self, topology):

        switches = [
            str(switch)
            for switch in topology.get(
                "switches",
                []
            )
        ]

        raw_links = topology.get(
            "links",
            []
        )

        links = []
        seen = set()

        for link in raw_links:

            source = str(
                link.get("source")
            )

            destination = str(
                link.get("destination")
            )

            link_key = tuple(
                sorted(
                    (
                        source,
                        destination,
                    )
                )
            )

            if link_key in seen:
                continue

            seen.add(link_key)

            links.append({
                "id": "-".join(link_key),
                "source": source,
                "destination": destination,
            })

        graph = self._build_graph(
            switches=switches,
            links=links,
        )

        reachability = self._build_reachability(
            graph
        )

        return {
            "hosts": [],
            "switches": switches,
            "links": links,
            "graph": graph,
            "reachability": reachability,
            "device_count": len(switches),
            "host_count": 0,
            "switch_count": len(switches),
            "link_count": len(links),
        }


    def _build_graph(
        self,
        switches,
        links,
    ):

        graph = {
            str(switch): []
            for switch in switches
        }

        for link in links:

            source = str(
                link["source"]
            )

            destination = str(
                link["destination"]
            )

            graph.setdefault(
                source,
                []
            )

            graph.setdefault(
                destination,
                []
            )

            if destination not in graph[source]:

                graph[source].append(
                    destination
                )

            if source not in graph[destination]:

                graph[destination].append(
                    source
                )

        return graph


    def _build_reachability(
        self,
        graph,
    ):

        reachability = {}

        for source in graph:

            visited = set()
            queue = [source]

            while queue:

                current = queue.pop(0)

                if current in visited:
                    continue

                visited.add(current)

                for neighbor in graph.get(
                    current,
                    []
                ):

                    if neighbor not in visited:

                        queue.append(
                            neighbor
                        )

            visited.discard(source)

            reachability[source] = sorted(
                visited
            )

        return reachability
