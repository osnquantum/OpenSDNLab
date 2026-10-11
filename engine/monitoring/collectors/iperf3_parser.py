"""Parse iperf3 JSON results into Mbps."""

import json
import math


def parse_iperf3_mbps(output):
    """
    Return received throughput in Mbps.

    Returns None when output is invalid or has no usable measurement.
    A measured throughput of 0.0 Mbps remains a valid result.
    """
    if not isinstance(output, str) or not output.strip():
        return None

    try:
        data = json.loads(output)
        value = data["end"]["sum_received"]["bits_per_second"]
        throughput_mbps = float(value)
    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        return None

    if not math.isfinite(throughput_mbps) or throughput_mbps < 0:
        return None

    return throughput_mbps / 1_000_000.0
