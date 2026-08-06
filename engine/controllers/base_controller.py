"""
Base SDN Controller
"""

from abc import ABC
from abc import abstractmethod


class BaseController(ABC):

    @abstractmethod
    def create(self, net):
        pass

    @abstractmethod
    def name(self):
        pass
