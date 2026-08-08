"""
OpenSDNLab Metrics Model

Research measurement metrics.
"""

from dataclasses import dataclass


@dataclass
class Metrics:

    ####################################################
    # Latency Metrics
    ####################################################

    average_rtt: float = 0.0

    minimum_rtt: float = 0.0

    maximum_rtt: float = 0.0

    delay: float = 0.0

    one_way_delay: float = 0.0

    latency_std: float = 0.0


    ####################################################
    # Reliability Metrics
    ####################################################

    packet_loss: float = 0.0

    packet_delivery_ratio: float = 0.0

    packets_sent: int = 0

    packets_received: int = 0


    ####################################################
    # Delay Variation
    ####################################################

    jitter: float = 0.0


    ####################################################
    # Performance Metrics
    ####################################################

    throughput: float = 0.0

    goodput: float = 0.0


    ####################################################
    # System Metrics
    ####################################################

    cpu_usage: float = 0.0

    memory_usage: float = 0.0


    ####################################################
    # SDN Metrics
    ####################################################

    flow_count: int = 0


    ####################################################
    # Experiment Metadata
    ####################################################

    experiment_time: float = 0.0
