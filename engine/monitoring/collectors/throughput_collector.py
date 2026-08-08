"""
Throughput Collector

Measures TCP throughput using iperf3.
"""

import re
import time

from engine.core.logger import logger

from engine.monitoring.collectors.base_collector import BaseCollector
from engine.monitoring.models.metrics import Metrics

from engine.metrics.metric_collector import MetricCollector


class ThroughputCollector(BaseCollector):


    ############################################################

    def collect(
        self,
        source,
        destination,
        experiment_id=None,
        duration=5
    ):

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

        collector = MetricCollector()


        match = re.search(

            r'([\d\.]+)\s+Mbits/sec',

            output

        )


        if match:

            metrics.throughput = float(

                match.group(1)

            )


            if experiment_id:

                collector.record(

                    experiment_id,

                    "throughput",

                    metrics.throughput,

                    node=source.name,


                )


        destination.cmd("pkill -f iperf3")


        return metrics
