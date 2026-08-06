"""
Controller Plugin Interface
"""

from abc import ABC, abstractmethod


class IControllerPlugin(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass
