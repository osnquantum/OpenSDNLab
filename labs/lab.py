"""
Laboratory Model
"""

from dataclasses import dataclass


@dataclass
class Lab:

    title: str

    objective: str

    theory: str

    scenario: object

    questions: list

    conclusion: str = ""
