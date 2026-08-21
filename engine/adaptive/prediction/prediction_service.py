"""
Network QoS Prediction Service
"""

from engine.adaptive.prediction.gru_predictor import (
    GRUPredictor
)


class PredictionService:


    def __init__(self):

        self.predictor = GRUPredictor()


    def predict(
        self,
        metrics_history
    ):

        return self.predictor.predict(
            metrics_history
        )


prediction_service = PredictionService()
