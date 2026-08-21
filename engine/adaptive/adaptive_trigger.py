"""
Adaptive Trigger Layer

Determines whether network conditions require
adaptive recovery.

Prediction and recovery remain independent.
"""


class AdaptiveTrigger:


    @staticmethod
    def evaluate(
        metrics,
        qos_decision,
        adaptive_status,
        prediction=None
    ):

        mode = adaptive_status["mode"]

        result = {

            "mode": mode,

            "prediction_enabled":
                adaptive_status[
                    "prediction_enabled"
                ],

            "recovery_enabled":
                adaptive_status[
                    "recovery_enabled"
                ],

            "triggered": False,

            "trigger_source": None,

            "degradation_detected": False,

            "prediction": prediction,

            "action": "NORMAL_OPERATION"
        }


        # -----------------------------------------
        # CURRENT NETWORK DEGRADATION
        # -----------------------------------------

        current_degradation = (
            qos_decision.get("action")
            != "NO_CHANGE"
        )


        # -----------------------------------------
        # PREDICTION OFF
        # -----------------------------------------

        if not adaptive_status[
            "prediction_enabled"
        ]:

            if current_degradation:

                result[
                    "degradation_detected"
                ] = True

                result[
                    "trigger_source"
                ] = "CURRENT_QOS"

                if adaptive_status[
                    "recovery_enabled"
                ]:

                    result[
                        "triggered"
                    ] = True

                    result[
                        "action"
                    ] = "REACTIVE_RECOVERY"

                else:

                    result[
                        "action"
                    ] = "DEGRADATION_MONITORED"


        # -----------------------------------------
        # PREDICTION ON
        # -----------------------------------------

        else:

            if prediction is not None:

                predicted_degradation = (
                    prediction.get(
                        "degradation_predicted",
                        False
                    )
                )

                if predicted_degradation:

                    result[
                        "degradation_detected"
                    ] = True

                    result[
                        "trigger_source"
                    ] = "PREDICTED_QOS"

                    if adaptive_status[
                        "recovery_enabled"
                    ]:

                        result[
                            "triggered"
                        ] = True

                        result[
                            "action"
                        ] = "PROACTIVE_RECOVERY"

                    else:

                        result[
                            "action"
                        ] = (
                            "PREDICTION_MONITORED"
                        )


        return result
