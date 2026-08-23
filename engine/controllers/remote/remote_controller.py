"""
Generic Remote SDN Controller

Supports:
- Ryu
- OS-Ken
- ONOS
- Floodlight
- OpenDaylight
- Faucet
- Any OpenFlow-compatible controller
"""

import socket

from mininet.node import RemoteController

from engine.controllers.base_controller import BaseController


class RemoteControllerAdapter(BaseController):

    def __init__(
        self,
        controller_name,
        ip="127.0.0.1",
        port=6653,
    ):

        self.controller_name = controller_name
        self.ip = ip
        self.port = int(port)

        self.controller = None

    ############################################################

    def create(self, net):

        self.controller = net.addController(

            self.controller_name,

            controller=RemoteController,

            ip=self.ip,

            port=self.port,

        )

        return self.controller

    ############################################################

    def start(self):

        """
        Remote controllers are managed externally.

        OpenSDNLab does not start OS-Ken/Ryu/etc. here.
        We simply verify that the configured controller
        is reachable.
        """

        return self.status()

    ############################################################

    def stop(self):

        """
        Do not terminate an externally managed controller.

        Only release the local adapter reference.
        """

        self.controller = None

        return True

    ############################################################

    def status(self):

        """
        Check whether the remote OpenFlow controller
        is accepting TCP connections.
        """

        try:

            with socket.create_connection(
                (
                    self.ip,
                    self.port,
                ),
                timeout=2,
            ):

                return {

                    "running": True,

                    "controller": self.controller_name,

                    "ip": self.ip,

                    "port": self.port,

                }

        except OSError:

            return {

                "running": False,

                "controller": self.controller_name,

                "ip": self.ip,

                "port": self.port,

            }

    ############################################################

    def name(self):

        return (
            f"Remote Controller "
            f"({self.controller_name})"
        )

    ############################################################

    def get_topology(self):

        """
        Remote controllers do not necessarily expose
        topology through a common API.

        Controller-specific topology discovery will be
        implemented by the appropriate controller plugin.
        """

        return {

            "switches": [],

            "links": [],

        }
