"""
Experiment Manager

Coordinates the complete experiment lifecycle.
"""

from uuid import uuid4

from engine.orchestration.system_manager import SystemManager
from engine.core.logger import logger
from engine.services.experiment_service import ExperimentService

from engine.network.blueprint.network_blueprint import NetworkBlueprint
from engine.network.managers.address_manager import AddressManager
from engine.network.inventory.inventory_manager import InventoryManager

from engine.deployment.deployment_manager import DeploymentManager

from engine.monitoring.monitoring_manager import MonitoringManager

from engine.repository.experiment_repository import ExperimentRepository
from engine.repository.sqlite.sqlite_repository import SQLiteRepository
from engine.analysis.statistics.analyzer import StatisticsAnalyzer
from engine.repository.models import ExperimentResult


class ExperimentManager:

    def __init__(self):

        self.system_manager = SystemManager()

        self.experiment_service = ExperimentService()

        self.address_manager = AddressManager()

        self.inventory_manager = InventoryManager()

        self.deployment_manager = DeploymentManager()

        self.monitoring_manager = MonitoringManager()

        self.repository = ExperimentRepository()

        self.sqlite_repository = SQLiteRepository()

        self.statistics = StatisticsAnalyzer()

    ############################################################

    def build_experiment(
        self,
        name,
        topology,
        hosts,
        switches,
        protocol,
        controller,
        addressing="ipv4",
    ):

        network = self.experiment_service.create_experiment(
            name=name,
            topology=topology,
            hosts=hosts,
            switches=switches,
            protocol=protocol,
            controller=controller,
        )

        blueprint = NetworkBlueprint.from_topology(
            network
        )

        self.address_manager.assign(
            blueprint,
            protocol=addressing,
        )

        inventory = self.inventory_manager.build(
        blueprint
        )

        inventory.metadata["topology"] = topology
        inventory.metadata["hosts"] = hosts
        inventory.metadata["switches"] = switches
        inventory.metadata["protocol"] = protocol
        inventory.metadata["controller"] = controller

        return inventory

    ############################################################

    def apply_deployment_profile(
        self,
        inventory,
        deployment,
    ):
        """
        Apply deployment settings to every link.
        """

        for link in inventory.links:

            link.bandwidth = deployment.get(
                "bandwidth",
                link.bandwidth,
            )

            link.delay = deployment.get(
                "delay",
                link.delay,
            )

            link.loss = deployment.get(
                "loss",
                link.loss,
            )
    ############################################################

    def deploy_experiment(
        self,
        inventory,
        controller_config,
    ):

        return self.deployment_manager.deploy(
            inventory,
            controller_config,
        )

    ############################################################

    def monitor_experiment(
        self,
        net,
        experiment_id,
    ):

        report = self.monitoring_manager.collect_all(
            net["h1"],
            net["h2"],
            experiment_id,
        )

        ping = report["ping"]

        throughput = report["throughput"]

        packet_capture = report["packet_capture"]

        return {

            "minimum_rtt": ping.minimum_rtt,

            "average_rtt": ping.average_rtt,

            "maximum_rtt": ping.maximum_rtt,

            "jitter": ping.jitter,

            "packet_loss": ping.packet_loss,

            "throughput": throughput.throughput,

            "one_way_delay": ping.average_rtt / 2,

        }

    ############################################################

    def create_result(
        self,
        experiment_name,
        inventory,
        metrics,
        protocol,
        controller,
        addressing="ipv4",
    ):

        link = inventory.links[0] if inventory.links else None

        return ExperimentResult(

            experiment_name=experiment_name,

            experiment_id=str(uuid4()),

            topology=inventory.metadata.get(
                "topology",
                "unknown",
            ),

            hosts=len(
                [
                    d
                    for d in inventory.devices
                    if d.device_type == "host"
                ]
            ),

            switches=len(
                [
                    d
                    for d in inventory.devices
                    if d.device_type == "switch"
                ]
            ),

            links=len(
                inventory.links
            ),

            protocol=protocol,

            controller=controller,

            bandwidth=link.bandwidth if link else 0,

            delay=link.delay if link else "",

            loss=link.loss if link else 0,

            minimum_rtt=metrics["minimum_rtt"],

            average_rtt=metrics["average_rtt"],

            maximum_rtt=metrics["maximum_rtt"],

            jitter=metrics["jitter"],

            packet_loss=metrics["packet_loss"],

            throughput=metrics["throughput"],

            one_way_delay=metrics["one_way_delay"],

        )
    ############################################################

    def save_result(
        self,
        result,
    ):

        json_file = self.repository.save(
            result
        )

        self.sqlite_repository.save(
            result
        )

        return json_file

    ############################################################

    def cleanup(self):

        try:

            self.deployment_manager.backend.stop()

        except Exception:

            pass

    ############################################################

    ############################################################
    # Execute one measurement run
    ############################################################

    def execute_single_run(
        self,
        config,
        experiment_id,
        run_number,
        job=None,
    ):

        logger.info(
            f"Starting measurement run {run_number}"
        )

        inventory = self.build_experiment(

            name=config.name,

            topology=config.topology["type"],

            hosts=config.topology["hosts"],

            switches=config.topology["switches"],

            protocol=config.network["protocol"],

            controller=config.controller["name"],

            addressing=config.network.get(
                "addressing",
                "ipv4"
            ),

        )


        self.apply_deployment_profile(
            inventory,
            config.deployment,
        )


        net = self.deploy_experiment(
            inventory,
            config.controller,
        )


        metrics = self.monitor_experiment(
            net,
            config.name,
        )


        self.sqlite_repository.save_run(
            experiment_id,
            run_number,
            metrics
        )


        self.cleanup()


        logger.info(
            f"Completed measurement run {run_number}"
        )


        return metrics


    ############################################################


    def run(
        self,
        config,
        job=None,
    ):

        experiment_id = str(uuid4())

        logger.info(
            f"Experiment ID: {experiment_id}"
        )

        logger.info('STEP 1: Preparing system')

        self.system_manager.controller_guard.check()

        if job:
            job.update_progress(
                10,
                "System prepared"
            )

        logger.info('STEP 2: Running experiment repetitions')


        total_runs = config.runs


        all_metrics = []


        for run_number in range(1, total_runs + 1):

            logger.info(
                f"Executing run {run_number}/{total_runs}"
            )


            metrics = self.execute_single_run(

                config,

                experiment_id,

                run_number,

                job

            )


            all_metrics.append(metrics)


            if job:

                progress = int(
                    20 + (70 * run_number / total_runs)
                )

                job.update_progress(

                    progress,

                    f"Run {run_number}/{total_runs} completed"

                )


        logger.info(
            "All measurement runs completed"
        )


        statistics_report = self.statistics.analyze(
            all_metrics
        )


        return {

            "runs": len(all_metrics),

            "measurements": all_metrics,

            "statistics": statistics_report

        }


    def run_batch(
        self,
        configurations,
    ):
        """
        Execute multiple experiment configurations.
        """

        results = []

        total = len(configurations)

        print()
        print("=" * 70)
        print(f"Executing {total} experiment(s)")
        print("=" * 70)

        for index, config in enumerate(
            configurations,
            start=1,
        ):

            print()
            print(f"[{index}/{total}] {config.name}")

            try:

                result = self.run(
                    config
                )

                results.append(
                    result
                )

            except Exception as error:

                print(
                    f"Experiment failed: {error}"
                )

        return results    ############################################################

    def run_batch(
        self,
        configurations,
    ):
        """
        Execute multiple experiment configurations.
        """

        results = []

        total = len(configurations)

        print()
        print("=" * 70)
        print(f"Executing {total} experiment(s)")
        print("=" * 70)

        for index, config in enumerate(
            configurations,
            start=1,
        ):

            print()
            print(f"[{index}/{total}] {config.name}")

            try:

                result = self.run(
                    config
                )

                results.append(
                    result
                )

            except Exception as error:

                print(
                    f"Experiment failed: {error}"
                )

        return results
