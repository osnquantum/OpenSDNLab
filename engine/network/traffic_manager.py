"""
OpenSDNLab Traffic Manager

Generates network traffic for experiments.
"""

from engine.core.logger import logger


class TrafficManager:


    def __init__(self):
        pass


    ############################################################

    def ping_test(
        self,
        source,
        destination
    ):

        logger.info(
            f"Ping test {source.name} -> {destination.name}"
        )


        result = source.cmd(
            f"ping -c 5 {destination.IP()}"
        )


        return result



    ############################################################

    def throughput_test(
        self,
        source,
        destination,
        duration=10
    ):

        logger.info(
            "Starting throughput test"
        )


        destination.cmd(
            "iperf -s -D"
        )


        result = source.cmd(
            f"iperf -c {destination.IP()} -t {duration}"
        )


        return result



    ############################################################

    def run(
        self,
        source,
        destination,
        traffic_type="TCP"
    ):


        report={}


        report["ping"] = self.ping_test(
            source,
            destination
        )


        report["throughput"] = self.throughput_test(
            source,
            destination
        )


        return report
