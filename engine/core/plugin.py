"""
OpenSDNLab Plugin Metadata
"""

from dataclasses import dataclass, field


@dataclass
class Plugin:

    id: str

    name: str

    version: str

    author: str

    category: str

    description: str

    supports: list = field(default_factory=list)
