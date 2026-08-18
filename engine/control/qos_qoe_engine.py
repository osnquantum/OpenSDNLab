"""
QoS-QoE Adaptive Decision Engine
"""


class QoSQoEEngine:


    def evaluate(
        self,
        mos,
        rtt,
        packet_loss,
        throughput
    ):

        decision = {
            "action": "NO_CHANGE",
            "reason": "Network performance acceptable"
        }


        # QoE degradation

        if mos is not None and mos < 3.5:

            return {
                "action": "OPTIMIZE_PATH",
                "reason": "Low QoE detected",
                "mos": mos
            }


        # Packet loss problem

        if packet_loss is not None and packet_loss > 5:

            return {
                "action": "REDUCE_CONGESTION",
                "reason": "High packet loss",
                "loss": packet_loss
            }


        # Latency problem

        if rtt is not None and rtt > 200:

            return {
                "action": "LATENCY_OPTIMIZATION",
                "reason": "High RTT",
                "rtt": rtt
            }


        return decision
