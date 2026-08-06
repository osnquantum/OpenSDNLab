"""
Ping Collector
"""

import re

from core.logger import logger

from monitoring.models.metrics import Metrics
from monitoring.collectors.base_collector import BaseCollector


class PingCollector(BaseCollector):

    ############################################################

    def collect(self, source, destination, count=4):

        logger.info(

            f"Pinging {destination.name} from {source.name}"

        )

        output = source.cmd(

            f"ping -c {count} {destination.IP()}"

        )

        metrics = Metrics()

        ########################################################

        loss = re.search(

            r'(\d+(?:\.\d+)?)% packet loss',

            output

        )

        if loss:

            metrics.packet_loss = float(

                loss.group(1)

            )

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

        return metrics
