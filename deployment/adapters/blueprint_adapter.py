"""
Blueprint Adapter

Converts NetworkBlueprint into a deployment plan.
"""

from core.logger import logger


class BlueprintAdapter:

    def convert(self, blueprint):

        logger.info("Converting blueprint to deployment plan")

        deployment_plan = {

            "experiment": blueprint.experiment_name,

            "protocol": blueprint.protocol,

            "controller": blueprint.controller,

            "hosts": [],

            "switches": [],

            "links": []

        }

        ############################################################

        for host in blueprint.hosts:

            deployment_plan["hosts"].append({

                "name": host.name,

                "ipv4": host.ipv4,

                "ipv6": host.ipv6,

                "mac": host.mac

            })

        ############################################################

        for switch in blueprint.switches:

            deployment_plan["switches"].append({

                "name": switch.name

            })

        ############################################################

        for link in blueprint.links:

            deployment_plan["links"].append({

                "source": link.source,

                "destination": link.destination,

                "bandwidth": link.bandwidth,

                "delay": link.delay,

                "loss": link.loss

            })

        logger.info("Deployment plan ready")

        return deployment_plan
