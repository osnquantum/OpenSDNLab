"""
Base Deployment Backend
"""

from abc import ABC
from abc import abstractmethod


class BaseBackend(ABC):

    @abstractmethod
    def deploy(self, blueprint):
        pass

    @abstractmethod
    def destroy(self):
        pass

    @abstractmethod
    def status(self):
        pass
