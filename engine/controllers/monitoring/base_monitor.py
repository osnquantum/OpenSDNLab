"""
Controller Monitoring Interface
"""

from abc import ABC, abstractmethod


class BaseControllerMonitor(ABC):

    @abstractmethod
    def collect(self, controller):
        pass
