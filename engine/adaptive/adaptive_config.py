"""
Adaptive Network Control Configuration
"""


class AdaptiveConfig:


    # Enable / disable QoS prediction

    PREDICTION_ENABLED = False


    # Enable / disable adaptive recovery

    RECOVERY_ENABLED = False


    # Prediction model

    PREDICTOR_TYPE = "GRU"


    # Minimum historical observations
    # required before prediction

    MIN_HISTORY = 5


    # Future prediction horizon

    PREDICTION_HORIZON = 1
