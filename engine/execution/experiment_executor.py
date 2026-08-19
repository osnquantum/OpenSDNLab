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
from engine.controllers.monitoring.controller_monitor import ControllerMonitor

class ExperimentExecutor:

    def __init__(self):

        self.topology_factory = TopologyFactory()

        self.inventory_manager = InventoryManager()

        self.backend = MininetBackend()

        self.controller_manager = ControllerManager()

        self.controller_monitor = ControllerMonitor()

        self.monitoring = MonitoringManager()

        self.traffic = TrafficManager()

        self.database = SQLiteRepository()

        self.metric_parser = MetricParser()

        self.qos_qoe_engine = QoSQoEEngine()

    def execute(self, experiment, job=None):

        CleanupManager.cleanup()

        RuntimeState.update(
            status="STARTING",
            experiment_id=experiment.experiment_id,
            stage="Cleanup",
            start_time=__import__("time").time(),
        )

        logger.info(f"Starting experiment {experiment.experiment_id}")

        # Use the complete custom topology when available.
        # Fall back to the legacy linear configuration.
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

        RuntimeState.update(
            stage="Topology Created",
            hosts=experiment.hosts,
            switches=experiment.switches,
        )

        controller = self.controller_manager.get(experiment.controller)

        controller_metrics = {}

        controller_info = controller.start()

        RuntimeState.update(
            stage="Controller Running",
            controller=str(experiment.controller),
            controller_metrics=controller_metrics
        )

        logger.info(controller_info)

        net = self.backend.deploy(inventory, controller)

        logger.info("Network deployed")

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

        decision = self.qos_qoe_engine.evaluate(
            mos=metrics["mos"],
            rtt=metrics["average_rtt"],
            packet_loss=metrics["packet_loss"],
            throughput=metrics["throughput"],
        )

        logger.info(f"QoS-QoE Decision: {decision}")

        RuntimeState.update(
            stage="Metrics Collected", metrics=metrics, decision=decision
        )

        previous = self.database.connection.execute(
            "SELECT MAX(run_number) FROM experiment_runs WHERE experiment_id=?",
            (experiment.experiment_id,),
        ).fetchone()[0]

        run_number = (previous or 0) + 1

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
            job_id=job
        )
        self.database.save_qos_qoe_decision(
            experiment.experiment_id, run_number, decision
        )

        logger.info("Stopping Mininet after successful experiment")

        try:
            self.backend.stop()

        except Exception:
            pass

        CleanupManager.cleanup()

        RuntimeState.update(status="COMPLETED", stage="Finished")

        return {"success": True, "experiment_id": experiment.experiment_id}
