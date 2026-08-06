"""
Base Analysis
"""

from abc import ABC, abstractmethod


class BaseAnalysis(ABC):

    @abstractmethod
    def generate_configurations(self):
        pass

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def compare(self, results):
        pass

    @abstractmethod
    def report(self, results):
        pass
