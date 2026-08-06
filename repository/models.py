"""
Experiment Result Model
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class ExperimentResult:

    ############################################################
    # Experiment
    ############################################################

    experiment_name: str
    experiment_id: str

    ############################################################
    # Network Configuration
    ############################################################

    topology: str
    hosts: int
    switches: int
    links: int

    protocol: str
    controller: str

    ############################################################
    # Link Configuration
    ############################################################

    bandwidth: float
    delay: str
    loss: float

    ############################################################
    # Performance Metrics
    ############################################################

    minimum_rtt: float
    average_rtt: float
    maximum_rtt: float

    jitter: float

    packet_loss: float

    throughput: float

    ############################################################

    created_at: datetime = datetime.now()

    status: str = "SUCCESS"

    notes: str = ""
