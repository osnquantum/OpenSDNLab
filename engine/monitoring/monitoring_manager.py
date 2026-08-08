"""
Monitoring Manager

Coordinates all experiment collectors.
"""

import time

from engine.monitoring.collectors.ping_collector import PingCollector
from engine.monitoring.collectors.throughput_collector import ThroughputCollector
from engine.monitoring.collectors.packet_capture_collector import PacketCaptureCollector


class MonitoringManager:


    def __init__(self):

        self.ping = PingCollector()

        self.throughput = ThroughputCollector()

        self.packet_capture = PacketCaptureCollector()



    ############################################################

    def wait_for_network(
        self,
        source,
        destination,
        retries=10
    ):

        for attempt in range(retries):

            result = source.cmd(
                f"ping -c 1 {destination.IP()}"
            )

            if "1 received" in result:

                return True

            time.sleep(1)


        return False



    ############################################################

    def collect_all(
        self,
        source,
        destination,
        experiment_id=None
    ):

        report = {}


        ########################################################
        # Network readiness check
        ########################################################

        self.wait_for_network(
            source,
            destination
        )


        ########################################################
        # Ping Metrics
        ########################################################

        report["ping"] = self.ping.collect(

            source,

            destination,

            experiment_id

        )


        ########################################################
        # Throughput Metrics
        ########################################################

        report["throughput"] = self.throughput.collect(

            source,

            destination,

            experiment_id

        )



        ########################################################
        # One-way Delay Packet Capture Metrics
        ########################################################

        report["packet_capture"] = self.packet_capture.collect(

            source,

            destination

        )


        return report
