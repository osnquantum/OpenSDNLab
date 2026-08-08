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

from engine.core.logger import logger


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


    def execute(self, experiment):

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


        ####################################################
        # 3. Start controller
        ####################################################

        controller = self.controller_manager.get(
            experiment.controller
        )


        controller_info = controller.start()


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


        ####################################################
        # 5. Generate Traffic
        ####################################################

        logger.info(
            "Starting traffic experiment"
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

        metrics = {

            "minimum_rtt": 0,

            "average_rtt": 0,

            "maximum_rtt": 0,

            "jitter": 0,

            "packet_loss": 0,

            "throughput": 0,

            "one_way_delay": 0

        }


        self.database.save_run(
            experiment.experiment_id,
            1,
            metrics
        )


        return {

            "success": True,

            "experiment_id":
                experiment.experiment_id

        }

