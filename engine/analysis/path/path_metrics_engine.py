"""
Path Metrics Engine.

Aggregates normalized logical link metrics into
path-level metrics for adaptive path selection.
"""


class PathMetricsEngine:

    def evaluate(
        self,
        path,
        link_metrics,
    ):
        """
        Evaluate a node path using normalized logical
        link metrics.

        Example path:

            [1, 2, 3]

        The engine evaluates:

            1 -> 2
            2 -> 3
        """

        if not path or len(path) < 2:
            return {
                "path": list(path or []),
                "hop_count": 0,
                "links_found": 0,
                "links_expected": 0,
                "measurement_complete": True,
                "throughput_mbps": 0.0,
                "packet_rate": 0.0,
                "total_errors": 0,
                "estimated_packet_loss": 0.0,
                "link_metrics": [],
            }

        path_links = []

        expected_links = len(path) - 1

        for index in range(expected_links):

            source = path[index]
            destination = path[index + 1]

            link = self._find_link(
                source=source,
                destination=destination,
                link_metrics=link_metrics,
            )

            if link is not None:
                path_links.append(link)

        links_found = len(path_links)

        measurement_complete = (
            links_found == expected_links
            and all(
                link.get(
                    "measurement_status",
                    {}
                ).get(
                    "complete",
                    False
                )
                for link in path_links
            )
        )

        if not path_links:
            return {
                "path": list(path),
                "hop_count": expected_links,
                "links_found": 0,
                "links_expected": expected_links,
                "measurement_complete": False,
                "throughput_mbps": 0.0,
                "packet_rate": 0.0,
                "total_errors": 0,
                "estimated_packet_loss": 0.0,
                "link_metrics": [],
            }

        throughput_values = [
            float(
                link.get(
                    "throughput_mbps",
                    0.0
                )
            )
            for link in path_links
        ]

        packet_rate_values = [
            float(
                link.get(
                    "packet_rate",
                    0.0
                )
            )
            for link in path_links
        ]

        total_errors = sum(
            int(
                link.get(
                    "total_errors",
                    0
                )
            )
            for link in path_links
        )

        # Throughput is constrained by the weakest
        # measured link on the path.
        throughput_mbps = min(
            throughput_values
        )

        # Packet rate is also represented by the
        # weakest measured hop.
        packet_rate = min(
            packet_rate_values
        )

        estimated_packet_loss = (
            self._calculate_packet_loss(
                path_links
            )
        )

        return {
            "path": list(path),
            "hop_count": expected_links,
            "links_found": links_found,
            "links_expected": expected_links,
            "measurement_complete":
                measurement_complete,
            "throughput_mbps":
                round(throughput_mbps, 4),
            "packet_rate":
                round(packet_rate, 4),
            "total_errors":
                total_errors,
            "estimated_packet_loss":
                round(
                    estimated_packet_loss,
                    6
                ),
            "link_metrics":
                path_links,
        }

    def _find_link(
        self,
        source,
        destination,
        link_metrics,
    ):
        """
        Find the normalized logical link connecting
        two switches.

        LinkMetricsEngine stores the switch DPIDs in:

            link["src"]["dpid"]
            link["dst"]["dpid"]
        """

        for link in link_metrics.values():

            src_dpid = (
                link.get(
                    "src",
                    {}
                ).get(
                    "dpid"
                )
            )

            dst_dpid = (
                link.get(
                    "dst",
                    {}
                ).get(
                    "dpid"
                )
            )

            if (
                src_dpid == source
                and dst_dpid == destination
            ):
                return link

            if (
                src_dpid == destination
                and dst_dpid == source
            ):
                return link

        return None

    def _calculate_packet_loss(
        self,
        path_links,
    ):
        """
        Estimate cumulative path packet loss from
        directional packet counters.

        For each logical link, directional imbalance
        is used as an estimated loss indicator.

        Path loss is calculated from cumulative
        success probability:

            path_loss =
                1 - product(1 - link_loss)
        """

        success_probability = 1.0

        for link in path_links:

            src_metrics = (
                link.get(
                    "src_port_metrics",
                    {}
                )
            )

            dst_metrics = (
                link.get(
                    "dst_port_metrics",
                    {}
                )
            )

            src_tx = float(
                src_metrics.get(
                    "tx_packets_delta",
                    0
                )
            )

            dst_rx = float(
                dst_metrics.get(
                    "rx_packets_delta",
                    0
                )
            )

            if src_tx <= 0:
                link_loss = 0.0

            else:
                delivered = min(
                    dst_rx,
                    src_tx
                )

                link_loss = (
                    max(
                        src_tx - delivered,
                        0.0
                    )
                    / src_tx
                )

            link_loss = min(
                max(link_loss, 0.0),
                1.0,
            )

            success_probability *= (
                1.0 - link_loss
            )

        return (
            1.0 - success_probability
        )


path_metrics_engine = (
    PathMetricsEngine()
)
