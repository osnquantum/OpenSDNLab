"""
Link Metrics Engine

Converts raw OpenFlow port statistics and topology
information into normalized logical link metrics.

The controller remains measurement-driven.

No static QoS degradation thresholds are defined here.
"""

import time


class LinkMetricsEngine:

    def build(
        self,
        link_map,
        port_metrics,
    ):

        logical_links = {}

        processed = set()

        for endpoint, link in link_map.items():

            src_dpid = link["src_dpid"]
            src_port = link["src_port"]

            dst_dpid = link["dst_dpid"]
            dst_port = link["dst_port"]

            # Normalize bidirectional links into one
            # logical link identifier.
            logical_id = tuple(
                sorted(
                    [
                        (
                            src_dpid,
                            src_port,
                        ),
                        (
                            dst_dpid,
                            dst_port,
                        ),
                    ]
                )
            )

            if logical_id in processed:
                continue

            processed.add(
                logical_id
            )

            src_key = (
                src_dpid,
                src_port,
            )

            dst_key = (
                dst_dpid,
                dst_port,
            )

            src_metrics = port_metrics.get(
                src_key
            )

            dst_metrics = port_metrics.get(
                dst_key
            )

            if (
                src_metrics is None
                or dst_metrics is None
            ):
                continue

            link_id = (
                f"s{src_dpid}:p{src_port}"
                f"<->"
                f"s{dst_dpid}:p{dst_port}"
            )

            throughput_mbps = round(
                (
                    src_metrics.get(
                        "throughput_mbps",
                        0,
                    )
                    +
                    dst_metrics.get(
                        "throughput_mbps",
                        0,
                    )
                )
                / 2,
                4,
            )

            packet_rate = round(
                (
                    src_metrics.get(
                        "packet_rate",
                        0,
                    )
                    +
                    dst_metrics.get(
                        "packet_rate",
                        0,
                    )
                )
                / 2,
                4,
            )

            tx_errors = (
                src_metrics.get(
                    "tx_errors_delta",
                    0,
                )
                +
                dst_metrics.get(
                    "tx_errors_delta",
                    0,
                )
            )

            rx_errors = (
                src_metrics.get(
                    "rx_errors_delta",
                    0,
                )
                +
                dst_metrics.get(
                    "rx_errors_delta",
                    0,
                )
            )

            total_errors = (
                tx_errors
                + rx_errors
            )

            logical_links[
                link_id
            ] = {

                "link_id":
                    link_id,

                "src": {
                    "dpid":
                        src_dpid,

                    "port":
                        src_port,
                },

                "dst": {
                    "dpid":
                        dst_dpid,

                    "port":
                        dst_port,
                },

                "timestamp":
                    time.time(),

                # Dynamic measurements

                "throughput_mbps":
                    throughput_mbps,

                "packet_rate":
                    packet_rate,

                "tx_errors":
                    tx_errors,

                "rx_errors":
                    rx_errors,

                "total_errors":
                    total_errors,

                # Raw directional references

                "src_port_metrics":
                    src_metrics,

                "dst_port_metrics":
                    dst_metrics,
            }

        return logical_links


link_metrics_engine = (
    LinkMetricsEngine()
)
