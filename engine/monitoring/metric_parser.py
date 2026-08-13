"""
OpenSDNLab Metric Parser

Extracts QoS metrics from ping and iperf output.
"""

import re

from engine.analysis.qos.mos_calculator import calculate_mos


class MetricParser:


    def parse_ping(self, output):

        metrics = {

            "minimum_rtt": 0.0,
            "average_rtt": 0.0,
            "maximum_rtt": 0.0,
            "jitter": 0.0,
            "packet_loss": 0.0

        }


        loss = re.search(
            r"(\d+)% packet loss",
            output
        )

        if loss:
            metrics["packet_loss"] = float(loss.group(1))


        rtt = re.search(
            r"=\s*([0-9.]+)/([0-9.]+)/([0-9.]+)/([0-9.]+)\s*ms",
            output
        )


        if rtt:

            metrics["minimum_rtt"] = float(rtt.group(1))

            metrics["average_rtt"] = float(rtt.group(2))

            metrics["maximum_rtt"] = float(rtt.group(3))

            metrics["jitter"] = float(rtt.group(4))


        return metrics



    def parse_iperf(self, output):

        throughput = 0.0


        result = re.search(
            r"([0-9.]+)\s+Mbits/sec\s*$",
            output
        )


        if result:

            throughput = float(
                result.group(1)
            )


        return throughput



    def parse(self, ping, iperf):


        metrics = self.parse_ping(
            ping
        )


        metrics["throughput"] = self.parse_iperf(
            iperf
        )


        metrics["one_way_delay"] = (
            metrics["average_rtt"] / 2
        )


        return metrics
