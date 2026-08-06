"""
Experiment Manager

Coordinates the complete experiment lifecycle.
"""

from engine.services.experiment_service import ExperimentService

from engine.network.blueprint.network_blueprint import NetworkBlueprint
from engine.network.managers.address_manager import AddressManager
from engine.network.inventory.inventory_manager import InventoryManager

from engine.deployment.deployment_manager import DeploymentManager

from engine.monitoring.monitoring_manager import MonitoringManager

from engine.repository.experiment_repository import ExperimentRepository
from engine.repository.sqlite.sqlite_repository import SQLiteRepository


class ExperimentManager:

    def __init__(self):

        self.experiment_service = ExperimentService()

        self.address_manager = AddressManager()

        self.inventory_manager = InventoryManager()

        self.deployment_manager = DeploymentManager()

        self.monitoring_manager = MonitoringManager()

        self.repository = ExperimentRepository()

        self.sqlite_repository = SQLiteRepository()

    ############################################################

    def build_experiment(self, name, topology, hosts, switches, protocol, controller):

        network = self.experiment_service.create_experiment(
            name=name,
            topology=topology,
            hosts=hosts,
            switches=switches,
            protocol=protocol,
            controller=controller,
        )

        blueprint = NetworkBlueprint.from_topology(network)

        self.address_manager.assign(blueprint, protocol=protocol)

        inventory = self.inventory_manager.build(blueprint)

        return inventory

    ############################################################

    def deploy_experiment(self, inventory, controller_config):

        net = self.deployment_manager.deploy(inventory, controller_config)

        return net

    ############################################################

    ############################################################

    def monitor_experiment(self, net):

        report = self.monitoring_manager.collect_all(net["h1"], net["h2"])

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

    def create_result(self, experiment_name, inventory, metrics, protocol, controller):

        from uuid import uuid4
        from engine.repository.models import ExperimentResult

        link = inventory.links[0] if inventory.links else None

        result = ExperimentResult(
            experiment_name=experiment_name,
            experiment_id=str(uuid4()),
            topology=inventory.metadata.get("topology", "unknown"),
            hosts=len([d for d in inventory.devices if d.device_type == "host"]),
            switches=len([d for d in inventory.devices if d.device_type == "switch"]),
            links=len(inventory.links),
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

        return result
        ############################################################

        def save_result(self, experiment_name, inventory, metrics):

            from engine.repository.models import ExperimentResult

            result = ExperimentResult(
                experiment_name=experiment_name,
                experiment_id="EXP-0001",
                topology=inventory.metadata.get("topology", "unknown"),
                hosts=len([d for d in inventory.devices if d.device_type == "host"]),
                switches=len(
                    [d for d in inventory.devices if d.device_type == "switch"]
                ),
                links=len(inventory.links),
                protocol="ipv4",
                controller="osken",
                bandwidth=inventory.links[0].bandwidth,
                delay=inventory.links[0].delay,
                loss=inventory.links[0].loss,
                minimum_rtt=metrics["minimum_rtt"],
                average_rtt=metrics["average_rtt"],
                maximum_rtt=metrics["maximum_rtt"],
                jitter=metrics["jitter"],
                packet_loss=metrics["packet_loss"],
                throughput=metrics["throughput"],
            )

            json_file = self.repository.save(result)

            self.sqlite_repository.save(result)

            return json_file

        ############################################################

        ############################################################

        def run(self, config):

            inventory = self.build_experiment(
                name=config.name,
                topology=config.topology["type"],
                hosts=config.topology["hosts"],
                switches=config.topology["switches"],
                protocol=config.network["protocol"],
                controller=config.controller["name"],
            )

            net = self.deploy_experiment(inventory, config.controller)

            metrics = self.monitor_experiment(net)

            filename = self.save_result(config.name, inventory, metrics)

            self.deployment_manager.backend.stop()

            return {"metrics": metrics, "result_file": str(filename)}

        ############################################################

        def run_batch(self, configurations):
            """
            Execute multiple experiment configurations.
            """

            results = []

            total = len(configurations)

            print()
            print("=" * 70)
            print(f"Executing {total} experiment(s)")
            print("=" * 70)

            for index, config in enumerate(configurations, start=1):

                print()
                print(f"[{index}/{total}] {config.name}")

                try:

                    result = self.run(config)

                    results.append(result)

                except Exception as error:

                    print(f"Experiment failed: {error}")

            return results
