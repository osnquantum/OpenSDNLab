"""
OpenSDNLab Mininet Backend
"""

from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController
from mininet.link import TCLink
from mininet.clean import cleanup

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
            autoSetMacs=True,
            autoStaticArp=True,
            controller=None,
            build=False
        )

        ########################################################
        # Configure the external SDN controller BEFORE starting
        # the Mininet network.
        ########################################################

        if controller:

            logger.info(
                f"Adding external controller on port {controller.port}"
            )

            self.net.addController(
                "c0",
                controller=RemoteController,
                ip="127.0.0.1",
                port=int(controller.port)
            )

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

            link_kwargs = {
                "bw": link.bandwidth,
                "delay": link.delay,
                "loss": link.loss,
                "max_queue_size": 1000
            }

            # Use explicit Mininet interface ports when provided.
            # None preserves Mininet's automatic port allocation.
            if link.source_port is not None:
                link_kwargs["port1"] = link.source_port

            if link.destination_port is not None:
                link_kwargs["port2"] = link.destination_port

            logger.info(
                f"Creating link {link.source} -> {link.destination} "
                f"(port1={link.source_port}, "
                f"port2={link.destination_port})"
            )

            self.net.addLink(
                src,
                dst,
                **link_kwargs
            )

        ########################################################

        logger.info("Building Mininet network")

        self.net.build()

        logger.info("Starting Mininet network")

        self.net.start()

        logger.info("Network started successfully")


        return self.net

    ############################################################

    def stop(self):

        if self.net:

            logger.info("Stopping network")

            self.net.stop()

            self.net = None
