"""
Traffic Plugin Interface
"""

from abc import ABC, abstractmethod


class ITrafficPlugin(ABC):

    @abstractmethod
    def generate(self):
        pass
