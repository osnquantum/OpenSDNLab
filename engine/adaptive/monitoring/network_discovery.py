"""
Network Discovery

Discovers hosts, switches and links from the existing
OpenSDNLab Inventory.
"""


class NetworkDiscovery:

    def discover(self, inventory):

        hosts = []
        switches = []
        links = []

        for device in inventory.devices:

            if device.device_type == "host":
                hosts.append(device.hostname)

            elif device.device_type == "switch":
                switches.append(device.hostname)

        for link in inventory.links:

            source = link.source
            destination = link.destination

            link_id = "-".join(
                sorted([source, destination])
            )

            links.append({
                "id": link_id,
                "source": source,
                "destination": destination,
                "bandwidth": getattr(link, "bandwidth", None),
                "delay": getattr(link, "delay", None),
                "loss": getattr(link, "loss", None)
            })

        return {
            "hosts": hosts,
            "switches": switches,
            "links": links,
            "device_count": len(inventory.devices),
            "host_count": len(hosts),
            "switch_count": len(switches),
            "link_count": len(links)
        }
