"""
Topology Object
"""

from dataclasses import dataclass, field


@dataclass
class Topology:

    name: str

    topology_type: str

    protocol: str

    controller: str

    hosts: list = field(default_factory=list)

    switches: list = field(default_factory=list)

    links: list = field(default_factory=list)

    metadata: dict = field(default_factory=dict)

    def summary(self):

        print()

        print("========== TOPOLOGY ==========")

        print(f"Name       : {self.name}")
        print(f"Type       : {self.topology_type}")
        print(f"Protocol   : {self.protocol}")
        print(f"Controller : {self.controller}")

        print(f"Hosts      : {len(self.hosts)}")
        print(f"Switches   : {len(self.switches)}")
        print(f"Links      : {len(self.links)}")

        print("==============================")

