from network.models import Host
from network.models import Switch
from network.models import Link
from network.models import Topology

topology = Topology(
    name="Experiment-1",
    topology_type="linear",
    protocol="ipv6",
    controller="ryu"
)

topology.hosts.append(Host("h1"))
topology.hosts.append(Host("h2"))

topology.switches.append(Switch("s1"))

topology.links.append(Link("h1", "s1"))
topology.links.append(Link("s1", "h2"))

topology.summary()
