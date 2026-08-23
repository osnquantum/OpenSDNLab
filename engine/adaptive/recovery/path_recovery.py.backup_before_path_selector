"""
Topology-Aware Path Recovery Strategy.

Analyzes the OpenSDNLab topology and determines
whether an alternative path exists.
"""

from engine.adaptive.recovery.base_recovery import (
    BaseRecovery
)

from engine.adaptive.recovery.topology_path_analyzer import (
    TopologyPathAnalyzer
)


class PathRecovery(BaseRecovery):


    def __init__(self):

        self.path_analyzer = (
            TopologyPathAnalyzer()
        )


    def execute(
        self,
        network,
        controller,
        metrics,
        trigger,
        inventory=None
    ):

        action = trigger.get(
            "action"
        )


        if action not in (
            "REACTIVE_RECOVERY",
            "PROACTIVE_RECOVERY"
        ):

            return {

                "executed": False,

                "success": False,

                "recovery_type":
                    "PATH_RECOVERY",

                "reason":
                    "No recovery action requested"

            }


        if network is None:

            return {

                "executed": False,

                "success": False,

                "recovery_type":
                    "PATH_RECOVERY",

                "reason":
                    "Network unavailable"

            }


        if inventory is None:

            return {

                "executed": False,

                "success": False,

                "recovery_type":
                    "PATH_RECOVERY",

                "reason":
                    "Topology inventory unavailable"

            }


        links = getattr(
            inventory,
            "links",
            []
        )


        if not links:

            return {

                "executed": False,

                "success": False,

                "recovery_type":
                    "PATH_RECOVERY",

                "reason":
                    "No topology links available"

            }


        hosts = getattr(
            network,
            "hosts",
            []
        )


        if len(hosts) < 2:

            return {

                "executed": False,

                "success": False,

                "recovery_type":
                    "PATH_RECOVERY",

                "reason":
                    "Insufficient hosts for path analysis"

            }


        source = hosts[0].name

        destination = hosts[-1].name


        analysis = self.path_analyzer.analyze(

            links=links,

            source=source,

            destination=destination

        )


        if not analysis[
            "alternative_path_available"
        ]:

            return {

                "executed": False,

                "success": False,

                "recovery_type":
                    "PATH_RECOVERY",

                "reason":
                    "No alternative path available",

                "path_analysis":
                    analysis

            }


        paths = analysis["paths"]

        primary_path = paths[0]

        alternative_path = paths[1]


        return {

            "executed": False,

            "success": True,

            "recovery_type":
                "PATH_RECOVERY",

            "reason":
                "Alternative path identified",

            "trigger_action":
                action,

            "primary_path":
                primary_path,

            "alternative_path":
                alternative_path,

            "path_analysis":
                analysis

        }
