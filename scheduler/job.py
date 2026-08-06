"""
Experiment Job
"""

from dataclasses import dataclass


@dataclass
class Job:

    id: int

    configuration: object

    status: str = "PENDING"
