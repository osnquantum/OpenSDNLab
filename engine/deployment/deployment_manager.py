"""
Deployment Manager

Coordinates deployment of an experiment.
"""

from engine.deployment.backends.mininet_backend import MininetBackend
from engine.controllers.controller_manager import ControllerManager


class DeploymentManager:

    def __init__(self):

        self.backend = MininetBackend()
        self.controller_manager = ControllerManager()

    ###########################################################

    def deploy(self, inventory, controller_config):

        controller = self.controller_manager.create(
            controller_config
        )

        return self.backend.deploy(
            inventory,
            controller
        )
