"""
Inventory Interface
"""

from dataclasses import dataclass


@dataclass
class Interface:

    name: str

    ipv4: str = ""

    ipv6: str = ""

    mac: str = ""

    mtu: int = 1500

