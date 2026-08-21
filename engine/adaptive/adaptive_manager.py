"""
Adaptive Network Control Manager

Supports:

- Prediction ON/OFF
- Recovery ON/OFF
- Reactive operation
- Proactive operation
"""

from engine.adaptive.adaptive_config import (
    AdaptiveConfig
)

from engine.adaptive.prediction.prediction_service import (
    prediction_service
)


class AdaptiveManager:


    def evaluate(
        self,
        metrics,
        metrics_history,
        prediction_enabled=False,
        recovery_enabled=False
    ):

        result = {

            "prediction_enabled":
                bool(prediction_enabled),

            "recovery_enabled":
                bool(recovery_enabled),

            "mode":
                "NORMAL",

            "prediction":
                None

        }


        # Prediction disabled
        # → normal/reactive operation

        if not prediction_enabled:

            result["mode"] = "REACTIVE"

            return result


        # Not enough historical data

        if (
            len(metrics_history)
            <
            AdaptiveConfig.MIN_HISTORY
        ):

            result["mode"] = "INSUFFICIENT_HISTORY"

            return result


        # Run prediction

        prediction = (
            prediction_service.predict(
                metrics_history
            )
        )

        result["prediction"] = prediction


        # Future degradation predicted

        if prediction.get(
            "degradation_predicted"
        ):

            result["mode"] = "PROACTIVE"

        else:

            result["mode"] = "NORMAL"


        return result


adaptive_manager = AdaptiveManager()
