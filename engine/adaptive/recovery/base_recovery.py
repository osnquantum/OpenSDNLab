"""
Base Recovery Strategy

Defines the interface for adaptive network
recovery mechanisms.
"""

from abc import ABC, abstractmethod


class BaseRecovery(ABC):


    @abstractmethod
    def execute(
        self,
        network,
        controller,
        metrics,
        trigger,
        inventory=None
    ):
        """
        Execute a recovery action.

        inventory contains the OpenSDNLab topology
        and link information when available.
        """

        raise NotImplementedError
