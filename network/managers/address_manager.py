"""
OpenSDNLab Address Manager

Automatically assigns IPv4, IPv6 and MAC addresses.
"""

from ipaddress import IPv4Network
from ipaddress import IPv6Network

from core.logger import logger


class AddressManager:

    def __init__(self):

        pass

    ###################################################################

    def assign(

        self,

        blueprint,

        protocol="ipv6",

        ipv4_prefix="10.0.0.0/24",

        ipv6_prefix="2001:db8::/64"

    ):

        logger.info("Assigning addresses")

        if protocol in ("ipv4", "dual"):

            self._assign_ipv4(
                blueprint,
                ipv4_prefix
            )

        if protocol in ("ipv6", "dual"):

            self._assign_ipv6(
                blueprint,
                ipv6_prefix
            )

        self._assign_mac(blueprint)

        logger.info("Address assignment complete")

        return blueprint

    ###################################################################

    def _assign_ipv4(self, blueprint, prefix):

        network = IPv4Network(prefix)

        hosts = list(network.hosts())

        for index, host in enumerate(blueprint.hosts):

            host.ipv4 = str(hosts[index])

    ###################################################################

    def _assign_ipv6(self, blueprint, prefix):

        network = IPv6Network(prefix)

        hosts = network.hosts()

        for host in blueprint.hosts:

            host.ipv6 = str(next(hosts))

    ###################################################################

    def _assign_mac(self, blueprint):

        for index, host in enumerate(blueprint.hosts, start=1):

            host.mac = (
                f"02:00:00:00:00:{index:02x}"
            )

