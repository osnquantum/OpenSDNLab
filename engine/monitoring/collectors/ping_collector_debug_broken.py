"""
Ping Collector
"""

import re

from engine.core.logger import logger

from engine.monitoring.models.metrics import Metrics
from engine.monitoring.collectors.base_collector import BaseCollector

from engine.metrics.metric_collector import MetricCollector


class PingCollector(BaseCollector):


    ############################################################

    def collect(
        self,
        source,
        destination,
        experiment_id=None,
        count=4
    ):

        logger.info(

            f"Pinging {destination.name} from {source.name}"

        )


        output = source.cmd(

            f"ping -c {count} {destination.IP()}"

        )

    logger.info(
        f"PING RAW OUTPUT: {output}"
    )


        metrics = Metrics()


        collector = MetricCollector()


        ########################################################
        # Packet Loss
        ########################################################

        loss = re.search(

            r'(\d+(?:\.\d+)?)% packet loss',

            output

        )


        if loss:

            metrics.packet_loss = float(

                loss.group(1)

            )


            if experiment_id:

                collector.record(

                    experiment_id,

                    "packet_loss",

                    metrics.packet_loss,

                    node=source.name,

                    device_type="host"

                )


        ########################################################
        # RTT and Jitter
        ########################################################

        rtt = re.search(

            r'=\s*([\d\.]+)/([\d\.]+)/([\d\.]+)/([\d\.]+)',

            output

        )


        if rtt:


            metrics.minimum_rtt = float(rtt.group(1))

            metrics.average_rtt = float(rtt.group(2))

            metrics.maximum_rtt = float(rtt.group(3))

            metrics.jitter = float(rtt.group(4))



            if experiment_id:


                collector.record(

                    experiment_id,

                    "rtt",

                    metrics.average_rtt,

                    node=source.name,

                    device_type="host"

                )


                collector.record(

                    experiment_id,

                    "jitter",

                    metrics.jitter,

                    node=source.name,

                    device_type="host"

                )


        return metrics
