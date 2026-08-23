"""
Intelligent Multi-Path Selector.

Ranks candidate paths using network health,
hop count, and optional QoS metrics.
"""


class PathSelector:

    def select_best_path(
        self,
        paths,
        network_health,
        qos_metrics=None,
        objective=None,
    ):

        qos_metrics = qos_metrics or {}
        ranked_paths = []

        for path in paths:

            # Reject paths containing unhealthy switches.
            unhealthy_nodes = [
                node
                for node in path
                if network_health.get(node)
                in ("UNRESPONSIVE", "DEGRADED")
            ]

            if unhealthy_nodes:
                continue

            hop_count = max(len(path) - 1, 0)

            # Health score: all remaining nodes are usable.
            health_score = 1.0

            # Prefer fewer hops.
            hop_score = 1.0 / (hop_count + 1)

            # Optional QoS scoring.
            qos_score = self._calculate_qos_score(
                qos_metrics
            )

            # Initial deterministic weighted score.
            score = (
                0.50 * health_score
                + 0.30 * hop_score
                + 0.20 * qos_score
            )

            ranked_paths.append({
                "path": path,
                "score": round(score, 4),
                "hop_count": hop_count,
                "health_score": health_score,
                "hop_score": round(hop_score, 4),
                "qos_score": round(qos_score, 4),
            })

        ranked_paths.sort(
            key=lambda item: item["score"],
            reverse=True,
        )

        best_path = (
            ranked_paths[0]["path"]
            if ranked_paths
            else None
        )

        return {
            "best_path": best_path,
            "ranked_paths": ranked_paths,
            "objective": objective,
        }

    def _calculate_qos_score(
        self,
        qos_metrics,
    ):

        if not qos_metrics:
            return 1.0

        score = 1.0

        packet_loss = qos_metrics.get(
            "packet_loss"
        )

        if packet_loss is not None:
            score -= min(
                float(packet_loss) / 100.0,
                1.0,
            ) * 0.4

        jitter = qos_metrics.get("jitter")

        if jitter is not None:
            score -= min(
                float(jitter) / 100.0,
                1.0,
            ) * 0.3

        average_rtt = qos_metrics.get(
            "average_rtt"
        )

        if average_rtt is not None:
            score -= min(
                float(average_rtt) / 1000.0,
                1.0,
            ) * 0.3

        return max(score, 0.0)
