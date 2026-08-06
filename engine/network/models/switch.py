from dataclasses import dataclass


@dataclass
class Switch:

    name: str

    dpid: str = ""
