"""
Controller Interface
"""

from abc import ABC, abstractmethod


class ControllerInterface(ABC):

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def restart(self):
        pass

    @abstractmethod
    def status(self):
        pass

