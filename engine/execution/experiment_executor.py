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


class ExperimentExecutor:


    def __init__(self):

        self.topology_factory = TopologyFactory()

        self.inventory_manager = InventoryManager()

        self.backend = MininetBackend()

        self.controller_manager = ControllerManager()

        self.monitoring = MonitoringManager()

        self.traffic = TrafficManager()
        self.database = SQLiteRepository()

        self.metric_parser = MetricParser()




    ########################################################


    def execute(self, experiment, job=None):

        CleanupManager.cleanup()

        RuntimeState.update(
            status="STARTING",
            experiment_id=experiment.experiment_id,
            stage="Cleanup",
            start_time=__import__("time").time()
        )

        logger.info(
            f"Starting experiment {experiment.experiment_id}"
        )


        ####################################################
        # 1. Create topology
        ####################################################

        topology = self.topology_factory.create(

            topology=experiment.topology,

            hosts=experiment.hosts,

            switches=experiment.switches,

            protocol=experiment.protocol,

            controller=experiment.controller,

            name=experiment.experiment_name

        )


        ####################################################
        # 2. Build inventory
        ####################################################

        inventory = self.inventory_manager.build(
            topology
        )

        RuntimeState.update(
            stage="Topology Created",
            hosts=experiment.hosts,
            switches=experiment.switches
        )


        ####################################################
        # 3. Start controller
        ####################################################

        controller = self.controller_manager.get(
            experiment.controller
        )


        controller_info = controller.start()


        RuntimeState.update(
            stage="Controller Running",
            controller=str(experiment.controller)
        )


        logger.info(
            controller_info
        )


        ####################################################
        # 4. Deploy Mininet
        ####################################################

        net = self.backend.deploy(
            inventory,
            controller
        )


        logger.info(
            "Network deployed"
        )


        import time

        logger.info(
            "Waiting for network stabilization"
        )

        time.sleep(5)


        ####################################################
        # 5. Generate Traffic
        ####################################################

        logger.info(
            "Starting traffic experiment"
        )

        RuntimeState.update(
            stage="Traffic Measurement"
        )


        traffic_report = self.traffic.run(
            net.hosts[0],
            net.hosts[-1]
        )


        logger.info(
            traffic_report
        )


        ####################################################
        # 6. Save Experiment Run
        ####################################################

        metrics = self.metric_parser.parse(
            traffic_report["ping"],
            traffic_report["throughput"]
        )

        RuntimeState.update(
            stage="Metrics Collected",
            metrics=metrics
        )


        previous = self.database.connection.execute(
            "SELECT MAX(run_number) FROM experiment_runs WHERE experiment_id=?",
            (experiment.experiment_id,)
        ).fetchone()[0]


        run_number = (previous or 0) + 1


        self.database.save_run(
            experiment.experiment_id,
            run_number,
            metrics
        )


        logger.info(
            "Stopping Mininet after successful experiment"
        )

        try:
            self.backend.stop()
        except Exception:
            pass


        CleanupManager.cleanup()


        RuntimeState.update(
            status="COMPLETED",
            stage="Finished"
        )

        return {

            "success": True,

            "experiment_id":
                experiment.experiment_id

        }

