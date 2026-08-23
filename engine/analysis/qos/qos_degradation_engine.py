"""
QoS Degradation Engine

Separates QoS degradation detection from
QoS/QoE decision selection.

The engine evaluates current QoS metrics against
a configurable degradation profile and returns
a normalized degradation state.
"""


class QoSDegradationEngine:

    NORMAL = "NORMAL"
    DEGRADED = "DEGRADED"
    CRITICAL = "CRITICAL"
    UNKNOWN = "UNKNOWN"


    DEFAULT_PROFILE = {

        "average_rtt": {
            "degraded": 100.0,
            "critical": 200.0,
            "direction": "higher"
        },

        "jitter": {
            "degraded": 30.0,
            "critical": 50.0,
            "direction": "higher"
        },

        "packet_loss": {
            "degraded": 2.0,
            "critical": 5.0,
            "direction": "higher"
        },

        "throughput": {
            "degraded": 10.0,
            "critical": 5.0,
            "direction": "lower"
        },

        "mos": {
            "degraded": 3.5,
            "critical": 2.5,
            "direction": "lower"
        }
    }


    def __init__(self, profile=None):

        self.profile = (
            profile
            if profile is not None
            else self.DEFAULT_PROFILE
        )


    def evaluate(self, metrics):

        metric_states = {}

        affected_metrics = []

        critical_metrics = []

        degraded_metrics = []


        for metric_name, rules in self.profile.items():

            value = metrics.get(metric_name)

            if value is None:

                metric_states[metric_name] = (
                    self.UNKNOWN
                )

                continue


            try:

                value = float(value)

            except (
                TypeError,
                ValueError
            ):

                metric_states[metric_name] = (
                    self.UNKNOWN
                )

                continue


            state = self._evaluate_metric(
                value=value,
                rules=rules
            )


            metric_states[
                metric_name
            ] = state


            if state == self.CRITICAL:

                affected_metrics.append(
                    metric_name
                )

                critical_metrics.append(
                    metric_name
                )


            elif state == self.DEGRADED:

                affected_metrics.append(
                    metric_name
                )

                degraded_metrics.append(
                    metric_name
                )


        if critical_metrics:

            severity = self.CRITICAL

        elif degraded_metrics:

            severity = self.DEGRADED

        else:

            severity = self.NORMAL


        return {

            "degradation_detected":
                severity
                != self.NORMAL,

            "severity":
                severity,

            "affected_metrics":
                affected_metrics,

            "critical_metrics":
                critical_metrics,

            "degraded_metrics":
                degraded_metrics,

            "metric_states":
                metric_states
        }


    def _evaluate_metric(
        self,
        value,
        rules
    ):

        direction = rules.get(
            "direction"
        )


        degraded = rules.get(
            "degraded"
        )


        critical = rules.get(
            "critical"
        )


        if direction == "higher":

            if (
                critical is not None
                and value >= critical
            ):

                return self.CRITICAL


            if (
                degraded is not None
                and value >= degraded
            ):

                return self.DEGRADED


        elif direction == "lower":

            if (
                critical is not None
                and value <= critical
            ):

                return self.CRITICAL


            if (
                degraded is not None
                and value <= degraded
            ):

                return self.DEGRADED


        return self.NORMAL


qos_degradation_engine = (
    QoSDegradationEngine()
)
