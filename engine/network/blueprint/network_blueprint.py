"""
OpenSDNLab Network Blueprint

A deployment-independent representation of a network.
"""

from dataclasses import dataclass, field
import json


@dataclass
class NetworkBlueprint:

    experiment_name: str

    protocol: str

    controller: str

    hosts: list = field(default_factory=list)

    switches: list = field(default_factory=list)

    links: list = field(default_factory=list)

    metadata: dict = field(default_factory=dict)

    ##############################################################

    @classmethod
    def from_topology(cls, topology):

        blueprint = cls(

            experiment_name=topology.name,

            protocol=topology.protocol,

            controller=topology.controller

        )

        blueprint.hosts = topology.hosts

        blueprint.switches = topology.switches

        blueprint.links = topology.links

        blueprint.metadata = topology.metadata

        return blueprint

    ##############################################################

    def to_dict(self):

        return {

            "experiment_name": self.experiment_name,

            "protocol": self.protocol,

            "controller": self.controller,

            "hosts": [host.__dict__ for host in self.hosts],

            "switches": [sw.__dict__ for sw in self.switches],

            "links": [link.__dict__ for link in self.links],

            "metadata": self.metadata

        }

    ##############################################################

    def export_json(self, filename):

        with open(filename, "w") as file:

            json.dump(

                self.to_dict(),

                file,

                indent=4

            )

    ##############################################################

    def summary(self):

        print()

        print("=========== BLUEPRINT ===========")

        print(f"Experiment : {self.experiment_name}")

        print(f"Protocol   : {self.protocol}")

        print(f"Controller : {self.controller}")

        print(f"Hosts      : {len(self.hosts)}")

        print(f"Switches   : {len(self.switches)}")

        print(f"Links      : {len(self.links)}")

        print("=================================")

        print()
