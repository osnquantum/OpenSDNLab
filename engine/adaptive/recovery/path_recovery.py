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

from engine.adaptive.recovery.path_selector import (
    PathSelector
)


class PathRecovery(BaseRecovery):


    def __init__(self):

        self.path_analyzer = (
            TopologyPathAnalyzer()
        )

        self.path_selector = (
            PathSelector()
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

                "path_recovery_status":
                    "PATH_RECOVERY_NO_ALTERNATIVE_PATH",

                "path_analysis":
                    analysis

            }


        paths = analysis["paths"]

        network_health = metrics.get(
            "network_health",
            {}
        )

        selection = (
            self.path_selector.select_best_path(
                paths=paths,
                network_health=network_health,
                qos_metrics=metrics,
                objective=trigger.get(
                    "objective"
                ),
            )
        )

        best_path = selection.get(
            "best_path"
        )

        if best_path is None:

            return {

                "executed": False,

                "success": False,

                "recovery_type":
                    "PATH_RECOVERY",

                "reason":
                    "No healthy recovery path available",

                "path_analysis":
                    analysis,

                "path_selection":
                    selection,

            }

        primary_path = paths[0]

        if controller is None:

            return {

                "executed": False,

                "success": False,

                "recovery_type":
                    "PATH_RECOVERY",

                "reason":
                    "Controller unavailable for path enforcement",

                "primary_path":
                    primary_path,

                "best_path":
                    best_path,

                "path_selection":
                    selection,

                "path_analysis":
                    analysis,

            }


        apply_recovery_path = getattr(
            controller,
            "apply_recovery_path",
            None,
        )

        if not callable(apply_recovery_path):

            return {

                "executed": False,

                "success": False,

                "recovery_type":
                    "PATH_RECOVERY",

                "reason":
                    "Controller does not support path enforcement",

                "primary_path":
                    primary_path,

                "best_path":
                    best_path,

                "path_selection":
                    selection,

                "path_analysis":
                    analysis,

            }


        enforcement = apply_recovery_path(
            path=best_path,
            destination=destination,
        )

        executed = enforcement.get(
            "executed",
            False,
        )

        success = enforcement.get(
            "success",
            False,
        )


        return {

            "executed": executed,

            "success": success,

            "recovery_type":
                "PATH_RECOVERY",

            "reason":
                "Recovery path enforcement completed"
                if success
                else "Recovery path enforcement failed",

            "trigger_action":
                action,

            "primary_path":
                primary_path,

            "best_path":
                best_path,

            "enforcement":
                enforcement,

            "path_selection":
                selection,

            "path_analysis":
                analysis

        }
