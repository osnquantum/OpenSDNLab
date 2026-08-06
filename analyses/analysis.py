"""
Generic Analysis
"""

from dataclasses import dataclass, field


@dataclass
class Analysis:

    name: str

    description: str = ""

    variables: list = field(default_factory=list)
