"""
Topology Plugin Interface
"""

from abc import ABC, abstractmethod


class ITopologyPlugin(ABC):

    @abstractmethod
    def build(self):
        pass
