"""
Deployment Interface
"""

from abc import ABC, abstractmethod


class DeploymentInterface(ABC):

    @abstractmethod
    def deploy(self, inventory, controller):
        pass

    @abstractmethod
    def stop(self):
        pass

