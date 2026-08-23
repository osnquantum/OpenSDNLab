"""
Network Health Manager

Tracks runtime health of switches and detects
unresponsive intermediate network nodes.
"""


class NetworkHealthManager:

    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    UNRESPONSIVE = "UNRESPONSIVE"
    RECOVERING = "RECOVERING"
    UNKNOWN = "UNKNOWN"

    def __init__(self):

        self.node_health = {}

    def register_nodes(self, nodes):

        for node in nodes:

            if node not in self.node_health:

                self.node_health[node] = self.UNKNOWN


    def register_switches_from_inventory(self, inventory):

        switches = [

            device.hostname

            for device in inventory.devices

            if device.device_type == "switch"

        ]

        self.register_nodes(switches)

        return switches


    def register_switches_from_inventory(self, inventory):

        switches = [

            device.hostname

            for device in inventory.devices

            if device.device_type == "switch"

        ]

        self.register_nodes(switches)

        return switches

    def update_from_controller_stats(
        self,
        controller_stats,
        switches,
    ):

        self.register_nodes(switches)

        active_datapaths = set(
            controller_stats.get(
                "active_datapaths",
                [],
            )
        )

        # Default Mininet / OVS mapping:
        #
        # DPID 1 -> s1
        # DPID 2 -> s2
        # ...
        expected_datapaths = {

            switch: int(
                switch[1:]
            )

            for switch in switches

            if switch.startswith("s")
            and switch[1:].isdigit()

        }

        for switch, dpid in expected_datapaths.items():

            if dpid in active_datapaths:

                self.mark_healthy(switch)

            else:

                self.mark_unresponsive(switch)

        return self.get_state()


    def mark_healthy(self, node):

        self.node_health[node] = self.HEALTHY

    def mark_degraded(self, node):

        self.node_health[node] = self.DEGRADED

    def mark_unresponsive(self, node):

        self.node_health[node] = self.UNRESPONSIVE

    def mark_recovering(self, node):

        self.node_health[node] = self.RECOVERING

    def get_status(self, node):

        return self.node_health.get(
            node,
            self.UNKNOWN
        )

    def get_unresponsive_nodes(self):

        return [

            node
            for node, status
            in self.node_health.items()

            if status == self.UNRESPONSIVE
        ]

    def get_state(self):

        return dict(self.node_health)


    def get_health(self):

        return self.get_state()
