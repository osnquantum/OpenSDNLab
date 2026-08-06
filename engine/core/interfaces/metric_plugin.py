"""
Metric Plugin Interface
"""

from abc import ABC, abstractmethod


class IMetricPlugin(ABC):

    @abstractmethod
    def collect(self, *args, **kwargs):
        """
        Collect QoS metrics.
        """
        pass
