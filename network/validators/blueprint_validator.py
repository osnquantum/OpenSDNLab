"""
OpenSDNLab Blueprint Validator
"""

from core.logger import logger


class BlueprintValidator:

    def validate(self, blueprint):

        logger.info("Validating network blueprint")

        self._validate_hosts(blueprint)

        self._validate_switches(blueprint)

        self._validate_links(blueprint)

        logger.info("Blueprint validation successful")

        return True

    ###########################################################

    def _validate_hosts(self, blueprint):

        names = set()

        for host in blueprint.hosts:

            if host.name in names:

                raise ValueError(
                    f"Duplicate host: {host.name}"
                )

            names.add(host.name)

    ###########################################################

    def _validate_switches(self, blueprint):

        names = set()

        for switch in blueprint.switches:

            if switch.name in names:

                raise ValueError(
                    f"Duplicate switch: {switch.name}"
                )

            names.add(switch.name)

    ###########################################################

    def _validate_links(self, blueprint):

        nodes = {

            h.name for h in blueprint.hosts

        }

        nodes.update(

            s.name for s in blueprint.switches

        )

        for link in blueprint.links:

            if link.source not in nodes:

                raise ValueError(

                    f"{link.source} does not exist."

                )

            if link.destination not in nodes:

                raise ValueError(

                    f"{link.destination} does not exist."

                )
