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


        try:
            result = source.cmd(
                f"timeout 15 ping -c 5 {destination.IP()}"
            )

            logger.info(
                "Ping completed successfully"
            )

            return result

        except Exception as e:
            logger.exception(
                "Ping failed: %s",
                str(e)
            )
            raise



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


        try:
            destination.cmd(
                "iperf -s -D"
            )

            logger.info(
                "iperf server started"
            )

            result = source.cmd(
                f"timeout 20 iperf -c {destination.IP()} -t {duration}"
            )

            logger.info(
                "iperf completed successfully"
            )

            return result

        except Exception as e:
            logger.exception(
                "Throughput test failed: %s",
                str(e)
            )
            raise



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
