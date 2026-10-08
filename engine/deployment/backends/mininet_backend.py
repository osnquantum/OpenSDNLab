"""
OpenSDNLab Mininet Backend
"""

from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController
from mininet.link import TCLink

from engine.core.logger import logger


class MininetBackend:

    def __init__(self):

        self.net = None

    ############################################################

    def deploy(self, inventory, controller):

        logger.info(
            "Initializing Mininet without global cleanup"
        )

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
                "jitter": link.jitter,
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

    def apply_link_impairments(self, inventory):
        """
        Dynamically apply bandwidth, delay, jitter and loss
        to the interfaces of an already-running Mininet network.
        """

        if self.net is None:
            raise RuntimeError("Mininet network is not running")

        for link in inventory.links:

            src = self.net.get(link.source)
            dst = self.net.get(link.destination)

            src_intf = None
            dst_intf = None

            # Use explicit ports when available.
            if link.source_port is not None:
                src_intf = src.intf(
                    f"{link.source}-eth{link.source_port}"
                )

            if link.destination_port is not None:
                dst_intf = dst.intf(
                    f"{link.destination}-eth{link.destination_port}"
                )

            # Otherwise discover the interfaces connecting these nodes.
            if src_intf is None or dst_intf is None:
                connections = src.connectionsTo(dst)

                if not connections:
                    logger.warning(
                        f"No interface connection found for "
                        f"{link.source} <-> {link.destination}"
                    )
                    continue

                src_intf, dst_intf = connections[0]

            kwargs = {
                "bw": link.bandwidth,
                "delay": link.delay,
                "jitter": link.jitter,
                "loss": link.loss,
                "max_queue_size": 1000,
            }

            src_intf.config(**kwargs)
            dst_intf.config(**kwargs)

            logger.info(
                f"Applied link impairment: "
                f"{link.source}:{src_intf.name} <-> "
                f"{link.destination}:{dst_intf.name} "
                f"bw={link.bandwidth}, "
                f"delay={link.delay}, "
                f"jitter={link.jitter}, "
                f"loss={link.loss}"
            )

    ############################################################

    def stop(self):

        if self.net:

            logger.info("Stopping network")

            self.net.stop()

            self.net = None
