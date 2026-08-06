"""
Network Inventory
"""

from dataclasses import dataclass, field


@dataclass
class Inventory:

    experiment_name: str

    devices: list = field(default_factory=list)

    links: list = field(default_factory=list)

    metadata: dict = field(default_factory=dict)

    ###########################################################

    def summary(self):

        print()

        print("========== INVENTORY ==========")

        print(f"Experiment : {self.experiment_name}")

        print(f"Devices    : {len(self.devices)}")

        print(f"Links      : {len(self.links)}")

        print("===============================")

        print()
