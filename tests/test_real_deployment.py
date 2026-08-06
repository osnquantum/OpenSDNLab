from repository.experiment_repository import ExperimentRepository
from repository.models import ExperimentResult
from monitoring.monitoring_manager import MonitoringManager

from services.experiment_service import ExperimentService

from network.blueprint.network_blueprint import NetworkBlueprint
from network.managers.address_manager import AddressManager
from network.inventory.inventory_manager import InventoryManager

from deployment.deployment_manager import DeploymentManager

############################################################

service = ExperimentService()

topology = service.create_experiment(

    name="Real Deployment",

    topology="linear",

    hosts=2,

    switches=1,

    protocol="ipv4",

    controller="local"

)

############################################################

blueprint = NetworkBlueprint.from_topology(

    topology

)

AddressManager().assign(

    blueprint,

    protocol="ipv4"

)

############################################################

inventory = InventoryManager().build(

    blueprint

)

############################################################

deployment = DeploymentManager()

net = deployment.deploy(
    inventory,
    {
        "type": "remote",
        "name": "osken",
        "ip": "127.0.0.1",
        "port": 6653
    }
)

############################################################

print()

print("Nodes")

print("----------------")

print(net.hosts)

print(net.switches)

print()

print("Running pingAll()")

print("----------------")

net.pingAll()

############################################################




############################################################

monitor = MonitoringManager()

report = monitor.collect_all(

    net["h1"],

    net["h2"]

)

############################################################

print()

print("===================================")
print(" Experiment Metrics")
print("===================================")

ping = report["ping"]

print()

print("PING")
print("----")
print(f"Average RTT : {ping.average_rtt:.3f} ms")
print(f"Packet Loss : {ping.packet_loss:.1f} %")

throughput = report["throughput"]

print()

print("THROUGHPUT")
print("----------")
print(f"TCP Throughput : {throughput.throughput:.2f} Mbit/s")

print("===================================")


############################################################

repository = ExperimentRepository()

result = ExperimentResult(

    experiment_name="Real Deployment",

    experiment_id="EXP-0001",

    topology="linear",

    hosts=2,

    switches=1,

    links=len(inventory.links),

    protocol="ipv4",

    controller="osken",

    bandwidth=100,

    delay=inventory.links[0].delay,

    loss=inventory.links[0].loss,

    minimum_rtt=ping.minimum_rtt,

    average_rtt=ping.average_rtt,

    maximum_rtt=ping.maximum_rtt,

    jitter=ping.jitter,

    packet_loss=ping.packet_loss,

    throughput=throughput.throughput

)

filename = repository.save(result)

print()
print("Experiment saved to:")
print(filename)
#####################################################################

deployment.backend.stop()

print()

print("Deployment finished.")

