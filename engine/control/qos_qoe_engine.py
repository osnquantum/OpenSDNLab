"""
QoS-QoE Adaptive Decision Engine
"""


class QoSQoEEngine:


    def evaluate(
        self,
        mos,
        rtt,
        packet_loss,
        throughput,
        jitter=None
    ):

        """
        Evaluate network QoS and QoE metrics and
        select an adaptive action.
        """

        # --------------------------------------------------
        # QoE degradation
        # Highest priority because it represents
        # user-perceived service quality.
        # --------------------------------------------------

        if mos is not None and mos < 3.5:

            return {
                "action": "OPTIMIZE_PATH",
                "reason": "Low QoE detected",
                "mos": mos
            }


        # --------------------------------------------------
        # Packet loss
        # --------------------------------------------------

        if (
            packet_loss is not None
            and packet_loss > 5
        ):

            return {
                "action": "REDUCE_CONGESTION",
                "reason": "High packet loss detected",
                "loss": packet_loss
            }


        # --------------------------------------------------
        # High jitter
        # --------------------------------------------------

        if (
            jitter is not None
            and jitter > 50
        ):

            return {
                "action": "STABILIZE_TRAFFIC",
                "reason": "High jitter detected",
                "jitter": jitter
            }


        # --------------------------------------------------
        # High latency
        # --------------------------------------------------

        if (
            rtt is not None
            and rtt > 150
        ):

            return {
                "action": "LATENCY_OPTIMIZATION",
                "reason": "High RTT detected",
                "rtt": rtt
            }


        # --------------------------------------------------
        # Normal condition
        # --------------------------------------------------

        return {
            "action": "NO_CHANGE",
            "reason": "Network performance acceptable"
        }
