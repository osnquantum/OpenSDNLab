"""
Study Model
"""

from dataclasses import dataclass, field


@dataclass
class Study:

    title: str

    description: str

    analyses: list = field(default_factory=list)
