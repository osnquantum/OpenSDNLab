"""
Comparison Result
"""

from dataclasses import dataclass, field


@dataclass
class ComparisonResult:

    scenario: str

    results: list = field(default_factory=list)
