"""
Base topology builder.
"""

from abc import ABC
from abc import abstractmethod


class BaseBuilder(ABC):

    @abstractmethod
    def build(
        self,
        hosts,
        switches,
        protocol,
        controller,
        name
    ):
        pass
