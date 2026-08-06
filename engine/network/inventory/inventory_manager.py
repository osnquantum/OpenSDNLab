"""
Inventory Manager

Builds a deployable inventory from a blueprint.
"""

from engine.network.inventory.inventory import Inventory
from engine.network.inventory.device import Device
from engine.network.inventory.interface import Interface

from engine.core.logger import logger


class InventoryManager:

    def build(self, blueprint):

        logger.info("Building inventory")

        inventory = Inventory(

            experiment_name=blueprint.experiment_name

        )

        device_id = 1

        #######################################################

        for host in blueprint.hosts:

            interface = Interface(

                name="eth0",

                ipv4=host.ipv4,

                ipv6=host.ipv6,

                mac=host.mac

            )

            inventory.devices.append(

                Device(

                    id=device_id,

                    hostname=host.name,

                    device_type="host",

                    interfaces=[interface]

                )

            )

            device_id += 1

        #######################################################

        for switch in blueprint.switches:

            inventory.devices.append(

                Device(

                    id=device_id,

                    hostname=switch.name,

                    device_type="switch"

                )

            )

            device_id += 1

        #######################################################

        inventory.links = blueprint.links

        logger.info("Inventory complete")

        return inventory
