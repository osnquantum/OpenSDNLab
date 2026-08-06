"""
Experiment Dataset

Standard dataset shared by all OpenSDNLab engines.
"""

from dataclasses import dataclass, field


@dataclass
class Dataset:

    name: str = ""

    rows: list = field(default_factory=list)

    metadata: dict = field(default_factory=dict)
