"""
Inventory Device
"""

from dataclasses import dataclass, field


@dataclass
class Device:

    id: int

    hostname: str

    device_type: str

    interfaces: list = field(default_factory=list)

    services: list = field(default_factory=list)

    metadata: dict = field(default_factory=dict)

