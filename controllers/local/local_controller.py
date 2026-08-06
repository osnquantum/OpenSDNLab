"""
Local Mininet Controller
"""

from mininet.node import Controller

from controllers.base_controller import BaseController


class LocalController(BaseController):

    def create(self, net):

        return net.addController(
            "c0",
            controller=Controller
        )

    def name(self):

        return "Local Controller"
