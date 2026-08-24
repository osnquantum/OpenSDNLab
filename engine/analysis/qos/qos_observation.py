"""
Raw end-to-end QoS observation model.

This module stores measured QoS values without applying arbitrary
thresholds, normalization bounds, weights, or quality classifications.
"""

from dataclasses import dataclass, asdict
from typing import List, Optional
import time


@dataclass
class QoSObservation:
    """
    A single raw observation for an end-to-end monitoring flow.
    """

    flow_id: str

    source: str
    destination: str

    path: List[int]

    rtt_ms: Optional[float] = None
    delay_ms: Optional[float] = None
    jitter_ms: Optional[float] = None
    packet_loss_percent: Optional[float] = None
    throughput_mbps: Optional[float] = None

    timestamp: float = None

    def __post_init__(self):

        if self.timestamp is None:
            self.timestamp = time.time()

    def to_dict(self):

        return asdict(self)
