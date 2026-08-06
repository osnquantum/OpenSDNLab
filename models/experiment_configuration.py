"""
Experiment Configuration
"""

from dataclasses import dataclass, field


@dataclass
class ExperimentConfiguration:

    name: str

    topology: dict = field(default_factory=dict)

    network: dict = field(default_factory=dict)

    controller: dict = field(default_factory=dict)

    deployment: dict = field(default_factory=dict)

    monitoring: dict = field(default_factory=dict)

    metadata: dict = field(default_factory=dict)

