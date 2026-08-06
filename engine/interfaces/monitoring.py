"""
Monitoring Interface
"""

from abc import ABC, abstractmethod


class MonitoringInterface(ABC):

    @abstractmethod
    def collect(self, source, destination):
        pass

