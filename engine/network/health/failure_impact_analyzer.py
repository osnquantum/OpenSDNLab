"""
Network Failure Impact Analyzer

Analyzes the effect of unresponsive network nodes on
topology connectivity, affected links, and network partitions.
"""


class FailureImpactAnalyzer:

    def analyze(
        self,
        topology,
        unresponsive_nodes,
    ):

        # --------------------------------------------------
        # Normalize failed nodes
        # --------------------------------------------------

        failed_nodes = set(
            unresponsive_nodes or []
        )

        # --------------------------------------------------
        # Extract nodes and links
        # --------------------------------------------------

        nodes = self._extract_nodes(
            topology
        )

        links = self._extract_links(
            topology
        )

        # --------------------------------------------------
        # Find links directly affected by failed nodes
        # --------------------------------------------------

        affected_links = []

        healthy_links = []

        for link in links:

            source, destination = link

            if (
                source in failed_nodes
                or destination in failed_nodes
            ):

                affected_links.append(
                    (source, destination)
                )

            else:

                healthy_links.append(
                    (source, destination)
                )

        # --------------------------------------------------
        # Healthy network graph
        # --------------------------------------------------

        healthy_nodes = set(nodes) - failed_nodes

        graph = {

            node: set()

            for node in healthy_nodes

        }

        for source, destination in healthy_links:

            if (
                source in healthy_nodes
                and destination in healthy_nodes
            ):

                graph[source].add(destination)
                graph[destination].add(source)

        # --------------------------------------------------
        # Detect connected components / partitions
        # --------------------------------------------------

        components = self._find_components(
            graph
        )

        partition_detected = (
            len(components) > 1
            if healthy_nodes
            else False
        )

        # --------------------------------------------------
        # Recovery requirement
        # --------------------------------------------------

        recovery_required = bool(
            failed_nodes
        )

        return {

            "failed_nodes":
                sorted(failed_nodes),

            "affected_links":
                affected_links,

            "healthy_nodes":
                sorted(healthy_nodes),

            "network_partition_detected":
                partition_detected,

            "connected_components":
                components,

            "recovery_required":
                recovery_required,

        }

    # ======================================================
    # NODE EXTRACTION
    # ======================================================

    def _extract_nodes(
        self,
        topology,
    ):

        if hasattr(topology, "nodes"):

            nodes = topology.nodes

            if callable(nodes):

                nodes = nodes()

            return list(nodes)

        if hasattr(topology, "switches"):

            switches = topology.switches

            if callable(switches):

                switches = switches()

            return list(switches)

        return []

    # ======================================================
    # LINK EXTRACTION
    # ======================================================

    def _extract_links(
        self,
        topology,
    ):

        if hasattr(topology, "links"):

            links = topology.links

            if callable(links):

                links = links()

        else:

            return []

        normalized_links = []

        for link in links:

            if isinstance(
                link,
                (tuple, list),
            ) and len(link) >= 2:

                normalized_links.append(
                    (
                        str(link[0]),
                        str(link[1]),
                    )
                )

        return normalized_links

    # ======================================================
    # CONNECTED COMPONENT DETECTION
    # ======================================================

    def _find_components(
        self,
        graph,
    ):

        visited = set()

        components = []

        for node in graph:

            if node in visited:

                continue

            component = []

            stack = [node]

            while stack:

                current = stack.pop()

                if current in visited:

                    continue

                visited.add(current)

                component.append(
                    current
                )

                for neighbor in graph.get(
                    current,
                    set(),
                ):

                    if neighbor not in visited:

                        stack.append(
                            neighbor
                        )

            components.append(
                sorted(component)
            )

        return components
