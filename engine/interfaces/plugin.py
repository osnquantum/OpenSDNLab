"""
Plugin Interface
"""

from abc import ABC, abstractmethod


class PluginInterface(ABC):

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def version(self):
        pass

    @abstractmethod
    def initialize(self):
        pass

