"""
Controller Manager

Creates SDN controllers from configuration.
"""

from engine.controllers.local.local_controller import LocalController
from engine.controllers.remote.remote_controller import RemoteControllerAdapter


class ControllerManager:

    ############################################################

    def create(self, config):

        controller_type = config.get("type", "local")

        ########################################################

        if controller_type == "local":

            return LocalController()

        ########################################################

        elif controller_type == "remote":

            return RemoteControllerAdapter(

                controller_name=config["name"],

                ip=config.get("ip", "127.0.0.1"),

                port=config.get("port", 6653)

            )

        ########################################################

        raise ValueError(

            f"Unsupported controller type: {controller_type}"

        )

