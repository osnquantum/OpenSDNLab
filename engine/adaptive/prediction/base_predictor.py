"""
Base Interface for Network QoS Predictors
"""

from abc import ABC, abstractmethod


class BasePredictor(ABC):


    @abstractmethod
    def predict(
        self,
        metrics_history
    ):
        """
        Predict future network QoS state.
        """

        pass
