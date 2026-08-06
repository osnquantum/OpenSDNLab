"""
Generic Remote SDN Controller

Supports:
- Ryu
- ONOS
- Floodlight
- OpenDaylight
- Faucet
- Any OpenFlow-compatible controller
"""

from mininet.node import RemoteController

from controllers.base_controller import BaseController


class RemoteControllerAdapter(BaseController):

    def __init__(

        self,

        controller_name,

        ip="127.0.0.1",

        port=6653

    ):

        self.controller_name = controller_name
        self.ip = ip
        self.port = port

    ############################################################

    def create(self, net):

        return net.addController(

            self.controller_name,

            controller=RemoteController,

            ip=self.ip,

            port=self.port

        )

    ############################################################

    def name(self):

        return f"Remote Controller ({self.controller_name})"

