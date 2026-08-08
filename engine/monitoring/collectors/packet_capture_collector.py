"""
Packet Capture Collector

Research measurement collector.

Measures:
- One-way delay
- Packet timestamps
- Delay distribution

Source:
tcpdump packet timestamps
"""

import re
import time

from engine.core.logger import logger
from engine.monitoring.models.metrics import Metrics


class PacketCaptureCollector:


    def collect(
        self,
        source,
        destination,
        count=5
    ):

        metrics = Metrics()


        logger.info(
            f"Packet capture {source.name} -> {destination.name}"
        )


        #
        # Start capture on destination
        #

        destination.cmd(
            "pkill tcpdump"
        )

        destination.cmd(
            "tcpdump -tt -n icmp > /tmp/packet_capture.log 2>&1 &"
        )


        time.sleep(1)


        #
        # Generate packets
        #

        source.cmd(
            f"ping -c {count} {destination.IP()}"
        )


        time.sleep(1)


        #
        # Stop capture
        #

        destination.cmd(
            "pkill tcpdump"
        )


        output = destination.cmd(
            "cat /tmp/packet_capture.log"
        )


        timestamps = []


        for line in output.splitlines():

            match = re.search(
                r"(\d+\.\d+)",
                line
            )

            if match:

                timestamps.append(
                    float(match.group(1))
                )


        #
        # Calculate delay samples
        #

        if len(timestamps) >= 2:

            delays = []

            for i in range(1, len(timestamps)):

                delay = (
                    timestamps[i]
                    -
                    timestamps[i-1]
                ) * 1000


                delays.append(delay)


            metrics.one_way_delay = (
                sum(delays)
                /
                len(delays)
            )


            metrics.delay = metrics.one_way_delay


        return metrics
