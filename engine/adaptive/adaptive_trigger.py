"""
Adaptive Trigger Layer

Determines whether current or predicted network
conditions require adaptive path recovery.

Current QoS degradation is evaluated using the
QoS Degradation Engine.

Prediction and path recovery remain independent.
"""

from engine.analysis.qos.qos_degradation_engine import (
    qos_degradation_engine
)


class AdaptiveTrigger:


    @staticmethod
    def evaluate(
        metrics,
        qos_decision,
        adaptive_status,
        prediction=None
    ):

        mode = adaptive_status["mode"]


        # -----------------------------------------
        # CURRENT QOS DEGRADATION ANALYSIS
        # -----------------------------------------

        degradation = (
            qos_degradation_engine.evaluate(
                metrics
            )
        )


        current_degradation = (
            degradation.get(
                "degradation_detected",
                False
            )
        )


        result = {

            "mode":
                mode,

            "prediction_enabled":
                adaptive_status[
                    "prediction_enabled"
                ],

            "recovery_enabled":
                adaptive_status[
                    "recovery_enabled"
                ],

            "triggered":
                False,

            "trigger_source":
                None,

            "degradation_detected":
                current_degradation,

            "severity":
                degradation.get(
                    "severity"
                ),

            "affected_metrics":
                degradation.get(
                    "affected_metrics",
                    []
                ),

            "critical_metrics":
                degradation.get(
                    "critical_metrics",
                    []
                ),

            "degraded_metrics":
                degradation.get(
                    "degraded_metrics",
                    []
                ),

            "metric_states":
                degradation.get(
                    "metric_states",
                    {}
                ),

            "prediction":
                prediction,

            "action":
                "NORMAL_OPERATION"
        }


        # -----------------------------------------
        # CURRENT NETWORK DEGRADATION
        # -----------------------------------------

        if current_degradation:

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
        # PREDICTED NETWORK DEGRADATION
        #
        # Prediction is evaluated independently.
        # It can trigger proactive recovery only
        # when current QoS has not already
        # triggered reactive recovery.
        # -----------------------------------------

        if (
            not result["triggered"]
            and adaptive_status[
                "prediction_enabled"
            ]
            and prediction is not None
        ):

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
