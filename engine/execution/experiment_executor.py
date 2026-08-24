"""
OpenSDNLab Experiment Executor

Coordinates complete SDN experiment lifecycle.
"""

from engine.network.factory.topology_factory import TopologyFactory
from engine.network.inventory.inventory_manager import InventoryManager

from engine.deployment.backends.mininet_backend import MininetBackend

from engine.controllers.manager.controller_manager import ControllerManager

from engine.monitoring.monitoring_manager import MonitoringManager

from engine.network.traffic_manager import TrafficManager
from engine.repository.sqlite.sqlite_repository import SQLiteRepository
from engine.monitoring.metric_parser import MetricParser
from engine.system.runtime_state import RuntimeState

from engine.core.logger import logger
from engine.system.cleanup_manager import CleanupManager
from engine.control.qos_qoe_engine import QoSQoEEngine
from engine.adaptive.adaptive_manager import AdaptiveManager
from engine.adaptive.adaptive_trigger import AdaptiveTrigger
from engine.adaptive.recovery import recovery_manager
from engine.adaptive.adaptive_state import AdaptiveState
import json

from engine.analysis.qos.qos_observation import (
    QoSObservation,
)
from pathlib import Path
from engine.controllers.monitoring.controller_monitor import ControllerMonitor
from engine.network.health.network_health_manager import NetworkHealthManager

class ExperimentExecutor:

    def __init__(self):

        self.topology_factory = TopologyFactory()

        self.inventory_manager = InventoryManager()

        self.backend = MininetBackend()

        self.controller_manager = ControllerManager()

        self.controller_monitor = ControllerMonitor()

        # Tracks real switch health using OS-Ken active datapaths.
        self.network_health = NetworkHealthManager()

        self.monitoring = MonitoringManager()

        self.traffic = TrafficManager()

        self.database = SQLiteRepository()

        self.metric_parser = MetricParser()

        self.qos_qoe_engine = QoSQoEEngine()

        # Adaptive QoS / prediction manager.
        self.adaptive_manager = AdaptiveManager()

        # Historical QoS observations for prediction.
        # This history is reset for each experiment.
        self.metrics_history = []

        # Reusable experiment runtime state.
        # A batch experiment can perform multiple measurement runs
        # on the same deployed Mininet topology.
        self.active_experiment_id = None
        self.active_network = None
        self.active_inventory = None
        self.active_controller = None

    def execute(
        self,
        experiment,
        job=None,
        run_number=1,
        total_runs=1
    ):

        # --------------------------------------------------------
        # Deploy topology once and reuse it for later runs.
        # --------------------------------------------------------

        if self.active_experiment_id != experiment.experiment_id:

            logger.info(
                f"Preparing experiment "
                f"{experiment.experiment_id}"
            )

            # Reset prediction history once per experiment.
            self.metrics_history = []

            CleanupManager.cleanup()

            RuntimeState.update(
                status="STARTING",
                experiment_id=experiment.experiment_id,
                stage="Preparing Network",
                start_time=__import__("time").time(),
            )

            # Use the complete custom topology when available.
            topology_config = getattr(
                experiment,
                "topology_data",
                None
            )

            if not isinstance(topology_config, dict):

                topology_config = {
                    "type": experiment.topology,
                    "hosts": experiment.hosts,
                    "switches": experiment.switches
                }

            topology = self.topology_factory.create(
                topology=topology_config.get(
                    "type",
                    "linear"
                ),
                hosts=topology_config.get(
                    "hosts",
                    experiment.hosts
                ),
                switches=topology_config.get(
                    "switches",
                    experiment.switches
                ),
                protocol=experiment.protocol,
                controller=experiment.controller,
                name=experiment.experiment_name,
                topology_data=topology_config,
            )

            inventory = self.inventory_manager.build(topology)

            # Register every switch so no intermediate node is left untracked.
            registered_switches = (
                self.network_health
                .register_switches_from_inventory(inventory)
            )

            logger.info(
                f"Registered switches for health monitoring: "
                f"{registered_switches}"
            )

            RuntimeState.update(
                stage="Topology Ready",
                hosts=experiment.hosts,
                switches=experiment.switches,
            )

            controller = self.controller_manager.get(
                experiment.controller
            )

            controller_metrics = {}

            controller_status = controller.status()

            if controller_status.get("running"):

                logger.info(
                    f"Controller {experiment.controller} "
                    "is already running. Reusing it."
                )

                controller_info = controller_status

            else:

                logger.info(
                    f"Starting controller: "
                    f"{experiment.controller}"
                )

                controller_info = controller.start()

            RuntimeState.update(
                stage="Controller Ready",
                controller=str(experiment.controller),
                controller_metrics=controller_metrics
            )

            logger.info(controller_info)

            net = self.backend.deploy(
                inventory,
                controller
            )

            logger.info("Network deployed")

            # Save reusable runtime objects.
            self.active_experiment_id = (
                experiment.experiment_id
            )
            self.active_network = net
            self.active_inventory = inventory
            self.active_controller = controller

        else:

            logger.info(
                f"Reusing deployed network for "
                f"experiment {experiment.experiment_id}"
            )

            net = self.active_network
            inventory = self.active_inventory
            controller = self.active_controller

            controller_metrics = {}

            RuntimeState.update(
                status="RUNNING",
                experiment_id=experiment.experiment_id,
                stage="Network Reused"
            )


        import time

        logger.info("Waiting for network stabilization")

        time.sleep(5)

        logger.info("Starting traffic experiment")

        print("===== TRAFFIC DEBUG 1 =====", flush=True)

        RuntimeState.update(stage="Traffic Measurement")

        print("===== TRAFFIC DEBUG 2 =====", flush=True)

        print(
            f"===== TRAFFIC HOSTS: {net.hosts[0].name} -> "
            f"{net.hosts[-1].name} =====",
            flush=True
        )

        print("===== TRAFFIC DEBUG 3 =====", flush=True)

        traffic_report = self.traffic.run(
            net.hosts[0],
            net.hosts[-1]
        )

        print("===== TRAFFIC DEBUG 4 =====", flush=True)

        logger.info(traffic_report)

        logger.info("Batch DEBUG: traffic completed")

        metrics = self.metric_parser.parse(
            traffic_report["ping"], traffic_report["throughput"]
        )

        logger.info(
            f"Batch DEBUG: metrics parsed: {metrics}"
        )

        # Resolve the actual forwarding path from the
        # controller-exported flow_paths. The controller is the
        # source of truth because it calculated and installed the
        # forwarding path for the Ethernet flow.
        controller_stats = {}

        controller_stats_path = Path(
            "runtime/controller_stats/osken.json"
        )

        if controller_stats_path.exists():
            try:
                with controller_stats_path.open() as f:
                    controller_stats = json.load(f)
            except Exception as exc:
                logger.warning(
                    f"Unable to read controller stats: {exc}"
                )

        source_host = net.hosts[0]
        destination_host = net.hosts[-1]

        source_mac = source_host.MAC()
        destination_mac = destination_host.MAC()

        flow_path_key = (
            f"{source_mac}->{destination_mac}"
        )

        flow_path = controller_stats.get(
            "flow_paths",
            {}
        ).get(
            flow_path_key,
            []
        )

        if not flow_path:
            logger.warning(
                f"No controller-resolved path found for {flow_path_key}"
            )

        logger.info(
            f"Controller-resolved path for {flow_path_key}: "
            f"{flow_path}"
        )

        # Create a standardized per-flow QoS observation directly
        # from experiment measurements and the controller-resolved
        # forwarding path.
        qos_observation = QoSObservation(
            flow_id=(
                f"{source_host.name}"
                f"->{destination_host.name}"
            ),
            source=source_host.name,
            destination=destination_host.name,
            path=flow_path,
            rtt_ms=metrics.get("average_rtt", 0.0),
            delay_ms=metrics.get("delay", 0.0),
            jitter_ms=metrics.get("jitter", 0.0),
            packet_loss_percent=metrics.get(
                "packet_loss",
                0.0
            ),
            throughput_mbps=metrics.get(
                "throughput",
                0.0
            ),
        )

        logger.info(
            f"QoS observation: "
            f"{qos_observation.to_dict()}"
        )

        # Build a common adaptive observation for
        # reactive QoS, GRU prediction, and DRL.
        # Current experiment traffic represents one active flow.
        # This is the initial data-plane observation and will later
        # be replaced by live OVS flow statistics.
        active_flows = 1

        adaptive_state = AdaptiveState.from_metrics(
            metrics,
            {
                "bandwidth": getattr(
                    experiment,
                    "bandwidth",
                    0.0
                ),
                "active_flows": active_flows,
                "hosts": experiment.hosts,
                "switches": experiment.switches,
                "controller": experiment.controller,
                "run_number": run_number,

                # Control-plane observation
                "controller_switch_count":
                    controller_stats.get("switch_count", 0),

                "topology_switch_count":
                    controller_stats.get(
                        "topology_switch_count",
                        0
                    ),

                "topology_link_count":
                    controller_stats.get(
                        "topology_link_count",
                        0
                    ),

                "packet_in_count":
                    controller_stats.get(
                        "packet_in_count",
                        0
                    ),

                "flow_install_count":
                    controller_stats.get(
                        "flow_install_count",
                        0
                    ),
            }
        )

        logger.info(
            f"Adaptive state: {adaptive_state}"
        )

        # --------------------------------------------------------
        # CONTROL-PLANE / NETWORK HEALTH
        # --------------------------------------------------------

        # Read live OS-Ken controller datapath statistics.
        stats_path = Path(
            "runtime/controller_stats/osken.json"
        )

        try:

            with stats_path.open() as f:
                controller_stats = json.load(f)

        except (
            FileNotFoundError,
            json.JSONDecodeError,
        ):

            logger.warning(
                "Controller stats unavailable; "
                "using empty datapath state"
            )

            controller_stats = {}

        registered_switches = [
            device.hostname
            for device in inventory.devices
            if device.device_type == "switch"
        ]

        self.network_health.update_from_controller_stats(
            controller_stats,
            registered_switches,
        )

        network_health_state = self.network_health.get_state()

        unresponsive_nodes = (
            self.network_health.get_unresponsive_nodes()
        )

        logger.info(
            f"Network health: {network_health_state}"
        )

        if unresponsive_nodes:

            logger.warning(
                f"Unresponsive network nodes detected: "
                f"{unresponsive_nodes}"
            )

        # --------------------------------------------------------

        # Store current QoS observation for prediction.
        self.metrics_history.append({

            "average_rtt":
                metrics["average_rtt"],

            "jitter":
                metrics["jitter"],

            "packet_loss":
                metrics["packet_loss"],

            "throughput":
                metrics["throughput"],

            "mos":
                metrics["mos"]

        })


        # Evaluate prediction / adaptive mode.
        adaptive_result = self.adaptive_manager.evaluate(

            metrics=metrics,

            metrics_history=
                self.metrics_history,

            prediction_enabled=
                getattr(
                    experiment,
                    "prediction_enabled",
                    False
                ),

            recovery_enabled=
                getattr(
                    experiment,
                    "recovery_enabled",
                    False
                )

        )


        logger.info(
            f"Adaptive result: {adaptive_result}"
        )


        decision = self.qos_qoe_engine.evaluate(
            mos=metrics["mos"],
            rtt=metrics["average_rtt"],
            packet_loss=metrics["packet_loss"],
            throughput=metrics["throughput"],
            jitter=metrics.get("jitter"),
        )

        logger.info(f"QoS-QoE Decision: {decision}")

        # Use the adaptive result calculated for THIS experiment.
        # This preserves per-experiment Prediction/Recovery settings.

        adaptive_status = adaptive_result


        logger.info(
            f"Adaptive Mode: "
            f"{adaptive_status['mode']}"
        )


        adaptive_trigger = (
            AdaptiveTrigger.evaluate(

                metrics=metrics,

                qos_decision=decision,

                adaptive_status=adaptive_status,

                prediction=
                    adaptive_result.get(
                        "prediction"
                    )

            )
        )

        logger.info(
            f"Adaptive Trigger: "
            f"{adaptive_trigger}"
        )


        ############################################################
        # Adaptive Recovery Execution
        ############################################################

        recovery_result = {

            "executed": False,

            "success": False,

            "reason":
                "Recovery not triggered"

        }


        if adaptive_trigger.get(
            "triggered",
            False
        ):

            recovery_result = (
                recovery_manager.execute(

                    strategy_name=
                        "PATH_RECOVERY",

                    network=
                        net,

                    controller=
                        controller,

                    metrics=
                        metrics,

                    trigger=
                        adaptive_trigger,

                    inventory=
                        inventory

                )
            )


        logger.info(
            f"Recovery result: "
            f"{recovery_result}"
        )

        # Normalize recovery state for API and dashboard.
        if not getattr(experiment, "recovery_enabled", False):

            path_recovery_status = "PATH_RECOVERY_DISABLED"

        elif not adaptive_trigger.get("triggered", False):

            path_recovery_status = "PATH_RECOVERY_NOT_REQUIRED"

        elif recovery_result.get(
            "path_recovery_status"
        ) == "PATH_RECOVERY_NO_ALTERNATIVE_PATH":

            path_recovery_status = (
                "PATH_RECOVERY_NO_ALTERNATIVE_PATH"
            )

        elif recovery_result.get("success", False):

            if recovery_result.get("executed", False):

                path_recovery_status = (
                    "PATH_RECOVERY_EXECUTED"
                )

            elif recovery_result.get("best_path"):

                path_recovery_status = (
                    "PATH_SELECTED"
                )

            else:

                path_recovery_status = (
                    "PATH_RECOVERY_TRIGGERED"
                )

        else:

            path_recovery_status = (
                "PATH_RECOVERY_FAILED"
            )


        recovery_result["path_recovery_status"] = path_recovery_status


        RuntimeState.update(
            stage="Metrics Collected",
            metrics=metrics,
            decision=decision,
            adaptive=adaptive_status,
            adaptive_trigger=adaptive_trigger,
            recovery=recovery_result
        )

        previous = self.database.connection.execute(
            "SELECT MAX(run_number) FROM experiment_runs WHERE experiment_id=?",
            (experiment.experiment_id,),
        ).fetchone()[0]

        run_number = (previous or 0) + 1


        # Save adaptive prediction / control state
        # separately from the reactive QoS-QoE decision.

        self.database.save_adaptive_decision(

            experiment_id=
                experiment.experiment_id,

            run_number=
                run_number,

            adaptive_result=
                adaptive_result,

            adaptive_trigger=
                adaptive_trigger

        )


        logger.info(

            "Adaptive decision saved: "

            f"experiment={experiment.experiment_id}, "

            f"run={run_number}, "

            f"mode={adaptive_result.get('mode')}"

        )


        logger.info("Batch DEBUG: collecting controller metrics")

        controller_metrics = self.controller_monitor.collect(
            controller
        )

        self.database.save_controller_metrics(
            experiment.experiment_id,
            run_number,
            controller.name(),
            controller_metrics["metrics"]
        )

        self.database.save_run(
            experiment.experiment_id,
            run_number,
            metrics,
            job_id=(
                job.id
                if hasattr(job, "id")
                else job
                if isinstance(job, str)
                else None
            )
        )
        self.database.save_qos_qoe_decision(
            experiment.experiment_id, run_number, decision
        )

        if run_number < total_runs:

            logger.info(
                f"Run {run_number}/{total_runs} completed. "
                "Keeping Mininet topology alive for the next run."
            )

            RuntimeState.update(
                status="RUNNING",
                experiment_id=experiment.experiment_id,
                stage=f"Run {run_number}/{total_runs} Completed"
            )

            return {
                "success": True,
                "experiment_id": experiment.experiment_id,
                "run_number": run_number,
                "total_runs": total_runs,
                "completed": False,
                "path_recovery_status": path_recovery_status,
                "path_recovery": recovery_result
            }

        logger.info(
            "Final run completed. Stopping Mininet topology."
        )

        try:
            self.backend.stop()

        except Exception as error:
            logger.warning(
                f"Error stopping Mininet: {error}"
            )

        CleanupManager.cleanup()

        self.active_experiment_id = None
        self.active_network = None
        self.active_inventory = None
        self.active_controller = None

        self.database.update_experiment_status(
            experiment.experiment_id,
            "COMPLETED"
        )

        logger.info(
            f"Experiment {experiment.experiment_id} marked as COMPLETED"
        )

        RuntimeState.update(
            status="COMPLETED",
            stage="Finished"
        )

        return {
            "success": True,
            "experiment_id": experiment.experiment_id,
            "run_number": run_number,
            "total_runs": total_runs,
            "completed": True,
            "path_recovery_status": path_recovery_status,
            "path_recovery": recovery_result
        }
