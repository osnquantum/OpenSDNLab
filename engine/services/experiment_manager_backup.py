"""
Experiment Manager

Coordinates the complete experiment lifecycle.
"""

from uuid import uuid4

from engine.orchestration.system_manager import SystemManager

from engine.services.experiment_service import ExperimentService

from engine.network.blueprint.network_blueprint import NetworkBlueprint
from engine.network.managers.address_manager import AddressManager
from engine.network.inventory.inventory_manager import InventoryManager

from engine.deployment.deployment_manager import DeploymentManager

from engine.monitoring.monitoring_manager import MonitoringManager

from engine.repository.experiment_repository import ExperimentRepository
from engine.repository.sqlite.sqlite_repository import SQLiteRepository
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

    ############################################################

    def build_experiment(
        self,
        name,
        topology,
        hosts,
        switches,
        protocol,
        controller,
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
            protocol=protocol,
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
    ):

        report = self.monitoring_manager.collect_all(
            net["h1"],
            net["h2"],
        )

        ping = report["ping"]

        throughput = report["throughput"]

        return {

            "minimum_rtt": ping.minimum_rtt,

            "average_rtt": ping.average_rtt,

            "maximum_rtt": ping.maximum_rtt,

            "jitter": ping.jitter,

            "packet_loss": ping.packet_loss,

            "throughput": throughput.throughput,

        }

    ############################################################

    def create_result(
        self,
        experiment_name,
        inventory,
        metrics,
        protocol,
        controller,
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

    def run(
        self,
        config,
    ):

        logger.info('STEP 1: Preparing system')

        self.system_manager.prepare()

        logger.info('STEP 2: Building experiment')

        inventory = self.build_experiment(

            name=config.name,

            topology=config.topology["type"],

            hosts=config.topology["hosts"],

            switches=config.topology["switches"],

            protocol=config.network["protocol"],

            controller=config.controller["name"],

        )

        logger.info('STEP 3: Applying deployment profile')

        self.apply_deployment_profile(

            inventory,

            config.deployment,

        )

        logger.info('STEP 4: Deploying Mininet')

        net = self.deploy_experiment(

            inventory,

            config.controller,

        )

        logger.info('STEP 5: Collecting metrics')

        metrics = self.monitor_experiment(
            net
        )

        result = self.create_result(

            experiment_name=config.name,

            inventory=inventory,

            metrics=metrics,

            protocol=config.network["protocol"],

            controller=config.controller["name"],

        )

        logger.info('STEP 6: Saving result')

        filename = self.save_result(
            result
        )

        self.cleanup()

        logger.info('EXPERIMENT COMPLETE')

        return {

            "result": result,

            "metrics": metrics,

            "result_file": str(filename),

        }
    ############################################################

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
