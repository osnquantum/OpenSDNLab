"""
OpenSDNLab QoS Decision Engine.

Evaluates live SDN link metrics and determines
the current network quality status.
"""


class QoSDecisionEngine:

    def __init__(
        self,
        warning_throughput_mbps=5.0,
        critical_throughput_mbps=10.0,
        warning_packet_rate=500.0,
        critical_packet_rate=1000.0,
        warning_errors=1,
        critical_errors=10,
    ):

        self.warning_throughput_mbps = (
            warning_throughput_mbps
        )

        self.critical_throughput_mbps = (
            critical_throughput_mbps
        )

        self.warning_packet_rate = (
            warning_packet_rate
        )

        self.critical_packet_rate = (
            critical_packet_rate
        )

        self.warning_errors = (
            warning_errors
        )

        self.critical_errors = (
            critical_errors
        )

    def evaluate(
        self,
        throughput_mbps,
        packet_rate,
        total_errors,
    ):

        critical = (
            throughput_mbps
            >= self.critical_throughput_mbps

            or packet_rate
            >= self.critical_packet_rate

            or total_errors
            >= self.critical_errors
        )

        if critical:

            return self._build_result(
                status="CRITICAL",
                throughput_mbps=throughput_mbps,
                packet_rate=packet_rate,
                total_errors=total_errors,
                quality_score=0.0,
            )

        warning = (
            throughput_mbps
            >= self.warning_throughput_mbps

            or packet_rate
            >= self.warning_packet_rate

            or total_errors
            >= self.warning_errors
        )

        if warning:

            return self._build_result(
                status="WARNING",
                throughput_mbps=throughput_mbps,
                packet_rate=packet_rate,
                total_errors=total_errors,
                quality_score=50.0,
            )

        return self._build_result(
            status="NORMAL",
            throughput_mbps=throughput_mbps,
            packet_rate=packet_rate,
            total_errors=total_errors,
            quality_score=100.0,
        )

    def _build_result(
        self,
        status,
        throughput_mbps,
        packet_rate,
        total_errors,
        quality_score,
    ):

        return {
            "status": status,
            "quality_score": quality_score,
            "throughput_mbps": throughput_mbps,
            "packet_rate": packet_rate,
            "total_errors": total_errors,
        }


qos_decision_engine = QoSDecisionEngine()
