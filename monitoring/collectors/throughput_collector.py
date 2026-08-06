"""
Throughput Collector

Measures TCP throughput using iperf3.
"""

import re
import time

from core.logger import logger

from monitoring.collectors.base_collector import BaseCollector
from monitoring.models.metrics import Metrics


class ThroughputCollector(BaseCollector):

    ############################################################

    def collect(self, source, destination, duration=5):

        logger.info(
            f"Measuring throughput from {source.name} to {destination.name}"
        )

        ########################################################
        # Start iperf3 server
        ########################################################

        destination.cmd("pkill -f iperf3")

        destination.cmd("iperf3 -s -D")

        time.sleep(1)

        ########################################################
        # Run client
        ########################################################

        output = source.cmd(

            f"iperf3 -c {destination.IP()} -t {duration}"

        )

        ########################################################

        metrics = Metrics()

        match = re.search(

            r'([\d\.]+)\s+Mbits/sec',

            output

        )

        if match:

            metrics.throughput = float(

                match.group(1)

            )

        destination.cmd("pkill -f iperf3")

        return metrics

