"""
Monitoring Manager

Coordinates all experiment collectors.
"""

from engine.monitoring.collectors.ping_collector import PingCollector
from engine.monitoring.collectors.throughput_collector import ThroughputCollector


class MonitoringManager:

    def __init__(self):

        self.ping = PingCollector()
        self.throughput = ThroughputCollector()

    ############################################################

    def collect_all(self, source, destination):

        report = {}

        ########################################################
        # Ping Metrics
        ########################################################

        report["ping"] = self.ping.collect(

            source,

            destination

        )

        ########################################################
        # Throughput Metrics
        ########################################################

        report["throughput"] = self.throughput.collect(

            source,

            destination

        )

        return report

