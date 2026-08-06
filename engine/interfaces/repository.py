"""
Repository Interface
"""

from abc import ABC, abstractmethod


class RepositoryInterface(ABC):

    @abstractmethod
    def save(self, result):
        pass

    @abstractmethod
    def load(self, experiment_id):
        pass

    @abstractmethod
    def delete(self, experiment_id):
        pass

