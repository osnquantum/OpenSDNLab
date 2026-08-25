"""
Intelligent Multi-Path Selector.

Ranks candidate paths using network health,
hop count, global QoS metrics, and optional
per-path QoS metrics.
"""


class PathSelector:

    def select_best_path(
        self,
        paths,
        network_health,
        qos_metrics=None,
        path_metrics=None,
        objective=None,
    ):

        qos_metrics = qos_metrics or {}
        path_metrics = path_metrics or {}

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

            hop_count = max(
                len(path) - 1,
                0,
            )

            # Remaining nodes are usable.
            health_score = 1.0

            # Prefer fewer hops.
            hop_score = 1.0 / (
                hop_count + 1
            )

            # Global end-to-end QoS score.
            global_qos_score = (
                self._calculate_qos_score(
                    qos_metrics
                )
            )

            # Retrieve metrics specific to this path.
            current_path_metrics = (
                self._get_path_metrics(
                    path=path,
                    path_metrics=path_metrics,
                )
            )

            path_qos_score = (
                self._calculate_path_qos_score(
                    current_path_metrics
                )
            )

            # Use path-specific QoS when available.
            qos_score = (
                path_qos_score
                if current_path_metrics
                else global_qos_score
            )

            # Weighted deterministic score.
            score = (
                0.40 * health_score
                + 0.25 * hop_score
                + 0.35 * qos_score
            )

            ranked_paths.append({
                "path": path,
                "score": round(
                    score,
                    4,
                ),
                "hop_count": hop_count,
                "health_score":
                    health_score,
                "hop_score": round(
                    hop_score,
                    4,
                ),
                "qos_score": round(
                    qos_score,
                    4,
                ),
                "path_metrics":
                    current_path_metrics,
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

    def _get_path_metrics(
        self,
        path,
        path_metrics,
    ):

        path_key = tuple(path)

        if path_key in path_metrics:
            return path_metrics[path_key]

        path_string = "->".join(
            str(node)
            for node in path
        )

        return path_metrics.get(
            path_string,
            {}
        )

    def _calculate_path_qos_score(
        self,
        metrics,
    ):

        if not metrics:
            return 1.0

        score = 1.0

        packet_loss = float(
            metrics.get(
                "estimated_packet_loss",
                0.0,
            )
        )

        # PathMetricsEngine returns loss as
        # a fraction between 0 and 1.
        score -= min(
            packet_loss,
            1.0,
        ) * 0.50

        measurement_complete = (
            metrics.get(
                "measurement_complete",
                False,
            )
        )

        if not measurement_complete:
            score -= 0.20

        total_errors = float(
            metrics.get(
                "total_errors",
                0,
            )
        )

        if total_errors > 0:
            error_penalty = min(
                total_errors / 100.0,
                1.0,
            )

            score -= (
                error_penalty
                * 0.20
            )

        throughput = float(
            metrics.get(
                "throughput_mbps",
                0.0,
            )
        )

        # A measured positive throughput gives
        # confidence that the path is active.
        if throughput <= 0:
            score -= 0.10

        return max(
            score,
            0.0,
        )

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

        jitter = qos_metrics.get(
            "jitter"
        )

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

        return max(
            score,
            0.0,
        )
