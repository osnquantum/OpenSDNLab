from network.factory.topology_factory import TopologyFactory

factory = TopologyFactory()

topology = factory.create(
    topology="linear",
    hosts=4,
    switches=2,
    protocol="ipv6",
    controller="ryu"
)

topology.summary()

print()

print("Hosts")

for host in topology.hosts:
    print(host)

print()

print("Switches")

for switch in topology.switches:
    print(switch)

print()

print("Links")

for link in topology.links:
    print(link)
