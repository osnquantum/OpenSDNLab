"""
Experiment Configuration
"""

from dataclasses import dataclass, field


@dataclass
class ExperimentConfiguration:

    ############################################################
    # Experiment
    ############################################################

    name: str

    ############################################################
    # Experiment Repetition
    ############################################################

    runs: int = 1


    ############################################################
    # Topology
    ############################################################

    topology: dict = field(default_factory=lambda: {
        "type": "linear",
        "hosts": 2,
        "switches": 1
    })

    ############################################################
    # Network
    ############################################################

    network: dict = field(default_factory=lambda: {
        "protocol": "ipv4"
    })

    ############################################################
    # Controller
    ############################################################

    controller: dict = field(default_factory=lambda: {
        "type": "remote",
        "name": "osken",
        "ip": "127.0.0.1",
        "port": 6653
    })

    ############################################################
    # Deployment
    ############################################################

    deployment: dict = field(default_factory=lambda: {
        "bandwidth": 100,
        "delay": "1ms",
        "loss": 0.0,
        "queue": 1000
    })

    ############################################################
    # Monitoring
    ############################################################

    monitoring: dict = field(default_factory=dict)

    ############################################################
    # Experiment Variables
    ############################################################

    variables: dict = field(default_factory=dict)

    ############################################################
    # Metadata
    ############################################################

    metadata: dict = field(default_factory=dict)

