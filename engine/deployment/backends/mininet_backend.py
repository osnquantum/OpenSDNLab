"""
OpenSDNLab Mininet Backend
"""

from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.link import TCLink

from engine.core.logger import logger


class MininetBackend:

    def __init__(self):

        self.net = None

    ############################################################

    def deploy(self, inventory, controller):

        logger.info("Initializing Mininet")

        self.net = Mininet(
            switch=OVSSwitch,
            link=TCLink,
            autoSetMacs=True
        )

        ########################################################

        logger.info("Creating controller")

        controller.create(self.net)

        ########################################################

        logger.info("Creating hosts")

        hosts = {}

        for device in inventory.devices:

            if device.device_type != "host":
                continue

            iface = device.interfaces[0]

            host = self.net.addHost(
                device.hostname,
                ip=iface.ipv4,
                mac=iface.mac
            )

            hosts[device.hostname] = host

        ########################################################

        logger.info("Creating switches")

        switches = {}

        for device in inventory.devices:

            if device.device_type != "switch":
                continue

            sw = self.net.addSwitch(
                device.hostname,
                protocols="OpenFlow13"
            )

            switches[device.hostname] = sw

        ########################################################

        logger.info("Creating links")

        for link in inventory.links:

            src = hosts.get(link.source)

            if src is None:
                src = switches[link.source]

            dst = hosts.get(link.destination)

            if dst is None:
                dst = switches[link.destination]

            self.net.addLink(
                src,
                dst,
                bw=link.bandwidth,
                delay=link.delay,
                loss=link.loss
            )

        ########################################################

        logger.info("Starting network")

        self.net.start()

        logger.info("Network started")

        return self.net

    ############################################################

    def stop(self):

        if self.net:

            logger.info("Stopping network")

            self.net.stop()

            self.net = None
