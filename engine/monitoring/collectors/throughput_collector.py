"""Measure TCP throughput using a bounded iperf3 JSON test."""

import secrets
import time

from engine.core.logger import logger
from engine.monitoring.collectors.base_collector import BaseCollector
from engine.monitoring.collectors.iperf3_parser import parse_iperf3_mbps
from engine.monitoring.models.metrics import Metrics
from engine.metrics.metric_collector import MetricCollector


def _is_expected_iperf_server(process_args, port):
    if not isinstance(process_args, str):
        return False
    args = process_args.split()
    return len(args) == 5 and args[0].endswith("iperf3") and args[1:5] == ["-s", "-1", "-p", str(port)]


class ThroughputCollector(BaseCollector):

    def collect(
        self,
        source,
        destination,
        experiment_id=None,
        duration=5
    ):
        logger.info(
            f"Measuring throughput from {source.name} to {destination.name}"
        )

        metrics = Metrics()
        metrics.throughput = None

        # Use a dedicated port and clean up only the server we start.
        port = 20000 + secrets.randbelow(20000)
        server_log = f"/tmp/opensdnlab_iperf3_{port}.log"
        server_pid = None

        try:
            server_output = destination.cmd(
                f"iperf3 -s -1 -p {port} "
                f"> {server_log} 2>&1 & echo $!"
            )

            # Mininet returns the background process PID from echo $!.
            for line in reversed(server_output.splitlines()):
                candidate = line.strip()
                if candidate.isdigit():
                    server_pid = int(candidate)
                    break

            if server_pid is None:
                logger.warning("Could not obtain iperf3 server PID")
                return metrics

            time.sleep(0.5)

            process_args = destination.cmd(
                f"ps -p {server_pid} -o args= 2>/dev/null"
            ).strip()

            server_status = destination.cmd(
                f"kill -0 {server_pid} 2>/dev/null; "
                f"printf 'SERVER_ALIVE:%s\\n' \"$?\"; "
                f"cat {server_log} 2>/dev/null"
            )

            if (
                not _is_expected_iperf_server(process_args, port)
                or "SERVER_ALIVE:0" not in server_status
                or "Address already in use" in server_status
                or "unable to start listener" in server_status.lower()
            ):
                logger.warning(
                    "iperf3 server failed identity or startup validation"
                )
                return metrics

            safe_duration = max(1, min(int(duration), 30))
            output = source.cmd(
                f"timeout {safe_duration + 8}s "
                f"iperf3 -c {destination.IP()} -p {port} "
                f"-t {safe_duration} -J"
            )

            throughput = parse_iperf3_mbps(output)

            if throughput is None:
                logger.warning(
                    f"Throughput measurement unavailable for "
                    f"{source.name} -> {destination.name}"
                )
                return metrics

            metrics.throughput = throughput

            if experiment_id:
                MetricCollector().record(
                    experiment_id,
                    "throughput",
                    throughput,
                    node=source.name,
                )

            logger.info(
                f"Measured throughput: {throughput:.6f} Mbps"
            )
            return metrics

        except Exception:
            logger.exception("Throughput measurement failed")
            return metrics

        finally:
            if server_pid is not None:
                process_args = destination.cmd(
                    f"ps -p {server_pid} -o args= 2>/dev/null"
                ).strip()

                if _is_expected_iperf_server(process_args, port):
                    destination.cmd(
                        f"kill {server_pid} 2>/dev/null || true"
                    )
