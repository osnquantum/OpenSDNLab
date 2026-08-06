"""
Experiment Insight
"""

from dataclasses import dataclass


@dataclass
class Insight:

    title: str

    observation: str

    explanation: str

    recommendation: str
