"""
OpenSDNLab Metrics Model
"""

from dataclasses import dataclass


@dataclass
class Metrics:

    average_rtt: float = 0.0
    minimum_rtt: float = 0.0
    maximum_rtt: float = 0.0

    packet_loss: float = 0.0

    jitter: float = 0.0

    delay: str = ""

    throughput: float = 0.0

    cpu_usage: float = 0.0

    memory_usage: float = 0.0

    flow_count: int = 0

    experiment_time: float = 0.0
