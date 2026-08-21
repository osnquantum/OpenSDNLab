"""
GRU-Based Network QoS Predictor

Input features:

- average_rtt
- jitter
- packet_loss
- throughput
- mos
"""

from engine.adaptive.prediction.base_predictor import (
    BasePredictor
)


class GRUPredictor(BasePredictor):


    FEATURES = [

        "average_rtt",

        "jitter",

        "packet_loss",

        "throughput",

        "mos"

    ]


    def __init__(self):

        self.model = None

        self.model_loaded = False


    def predict(
        self,
        metrics_history
    ):

        """
        Placeholder prediction interface.

        A trained GRU model will later receive
        a sequence of historical QoS measurements.
        """

        if not metrics_history:

            return {

                "prediction_available": False,

                "degradation_predicted": False,

                "reason":
                    "Insufficient historical QoS data"

            }


        return {

            "prediction_available": False,

            "degradation_predicted": False,

            "reason":
                "GRU model not trained yet"

        }
