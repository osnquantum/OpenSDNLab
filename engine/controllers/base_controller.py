"""
Base SDN Controller Interface
"""

from abc import ABC, abstractmethod


class BaseController(ABC):


    @abstractmethod
    def start(self):
        pass


    @abstractmethod
    def stop(self):
        pass


    @abstractmethod
    def status(self):
        pass


    @abstractmethod
    def name(self):
        pass
