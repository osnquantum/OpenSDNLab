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

        # Signature of the currently deployed data plane.
        # Used to decide whether a new GUI experiment can reuse
        # the existing Mininet topology.
        self.active_topology_signature = None

    def execute(
        self,
        experiment,
        job=None,
        run_number=1,
        total_runs=1
    ):

        # --------------------------------------------------------
        # DATA PLANE REUSE / TOPOLOGY COMPATIBILITY
        # --------------------------------------------------------
        #
        # Reuse the active Mininet data plane when the requested
        # topology matches the currently deployed topology.
        # Rebuild only when there is no active network or when the
        # topology structure/configuration has changed.

        import json

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

        requested_topology_signature = json.dumps(
            topology_config,
            sort_keys=True,
            default=str
        )

        topology_changed = (
            self.active_network is not None
            and self.active_topology_signature
            != requested_topology_signature
        )

        if self.active_network is None or topology_changed:

            logger.info(
                f"Preparing experiment "
                f"{experiment.experiment_id}"
            )

            # Reset prediction history once per experiment.
            self.metrics_history = []

            # Stop the previous managed controller before destroying
            # the old Mininet/OVS topology. A fresh controller will
            # discover the newly created topology.
            if self.active_controller:

                try:
                    self.controller_manager.stop(
                        experiment.controller
                    )

                except Exception as exc:

                    logger.warning(
                        f"Controller stop before cleanup failed: {exc}"
                    )

                self.active_controller = None

            CleanupManager.cleanup()

            RuntimeState.update(
                status="STARTING",
                experiment_id=experiment.experiment_id,
                stage="Preparing Network",
                start_time=__import__("time").time(),
            )

            if topology_changed:

                logger.info(
                    "Topology changed. Rebuilding Mininet data plane."
                )

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

            # --------------------------------------------------------
            # START / REUSE MANAGED CONTROLLER
            # --------------------------------------------------------

            controller = self.controller_manager.get(
                experiment.controller
            )

            controller_metrics = {}

            logger.info(
                f"Preparing controller: {experiment.controller}"
            )

            # Always delegate lifecycle management to
            # ControllerManager. The controller plugin decides
            # whether an existing managed controller can be reused
            # or whether a fresh OS-Ken process is required.
            controller_info = self.controller_manager.start(
                experiment.controller
            )

            # Refresh the controller reference after startup.
            controller = self.controller_manager.get(
                experiment.controller
            )

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

            self.active_topology_signature = (
                requested_topology_signature
            )

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

        # --------------------------------------------------------
        # POPULATE QOS MATRIX WITH MEASURED DATA
        # --------------------------------------------------------
        # The existing experiment metrics describe the primary
        # measurement flow. Preserve them and attach them to the
        # corresponding matrix row. Other concurrent flows remain
        # available for independent measurement in the next stage.

        if "qos_matrix" in locals() and qos_matrix:

            primary_flow = qos_matrix[0]

            primary_flow["rtt"] = metrics.get(
                "average_rtt",
                metrics.get("rtt")
            )

            primary_flow["jitter"] = metrics.get("jitter")

            primary_flow["packet_loss"] = metrics.get(
                "packet_loss"
            )

            primary_flow["throughput"] = metrics.get(
                "throughput"
            )

            logger.info(
                "Primary flow QoS matrix updated: "
                f"{primary_flow}"
            )

            RuntimeState.update(
                qos_matrix=qos_matrix
            )

        # --------------------------------------------------------
        # CONTROLLER STATS SYNCHRONIZATION
        # --------------------------------------------------------
        #
        # OS-Ken processes topology events, Packet-In messages and
        # OpenFlow statistics asynchronously. Traffic completion does
        # not guarantee that the controller has already exported its
        # latest state. Wait briefly for a complete controller snapshot
        # before using it for path resolution and adaptive QoS.
        import time

        controller_stats = {}

        controller_stats_path = Path(
            "runtime/controller_stats/osken.json"
        )

        expected_switches = len(
            [
                device
                for device in inventory.devices
                if device.device_type == "switch"
            ]
        )

        sync_timeout = 8
        sync_deadline = time.time() + sync_timeout

        logger.info(
            "Waiting for OS-Ken controller statistics: "
            f"expected_switches={expected_switches}"
        )

        while time.time() < sync_deadline:

            if controller_stats_path.exists():

                try:

                    with controller_stats_path.open() as f:
                        candidate_stats = json.load(f)

                    discovered_switches = candidate_stats.get(
                        "switch_count",
                        0
                    )

                    if (
                        discovered_switches >= expected_switches
                        and expected_switches > 0
                    ):

                        controller_stats = candidate_stats

                        logger.info(
                            "OS-Ken controller statistics synchronized: "
                            f"datapaths={discovered_switches}, "
                            f"packet_in="
                            f"{candidate_stats.get('packet_in_count', 0)}, "
                            f"flows="
                            f"{candidate_stats.get('flow_install_count', 0)}"
                        )

                        break

                    controller_stats = candidate_stats

                except (
                    OSError,
                    json.JSONDecodeError,
                ) as exc:

                    logger.warning(
                        f"Unable to read controller stats: {exc}"
                    )

            time.sleep(0.5)

        if not controller_stats:

            logger.warning(
                "OS-Ken statistics synchronization timed out; "
                "continuing with empty controller state"
            )

        # --------------------------------------------------------
        # CONTROLLER-DISCOVERED ACTIVE FLOWS
        # --------------------------------------------------------
        # The controller is the source of truth for active forwarding
        # flows. Do not create positional synthetic flows such as
        # h1->h5 based on topology order.

        available_hosts = list(net.hosts)

        host_by_mac = {
            host.MAC().lower(): host
            for host in available_hosts
        }

        # --------------------------------------------------------
        # ACTIVE FLOW DISCOVERY
        # --------------------------------------------------------
        # First use controller-known flows. If none exist yet, create
        # lightweight topology-derived probes so OS-Ken can learn host
        # locations and install forwarding paths. No positional flow
        # such as h1->h5 is hard-coded.

        traffic_flows = []

        controller_flow_paths = (
            controller_stats.get("flow_paths", {})
            if isinstance(controller_stats, dict)
            else {}
        )

        for flow_key in controller_flow_paths:

            try:
                source_mac, destination_mac = (
                    flow_key.split("->", 1)
                )

            except ValueError:

                logger.warning(
                    f"Invalid controller flow key ignored: "
                    f"{flow_key!r}"
                )
                continue

            flow_source = host_by_mac.get(
                source_mac.lower()
            )
            flow_destination = host_by_mac.get(
                destination_mac.lower()
            )

            if (
                flow_source is None
                or flow_destination is None
                or flow_source == flow_destination
            ):
                continue

            flow_pair = (
                flow_source,
                flow_destination,
            )

            if flow_pair not in traffic_flows:
                traffic_flows.append(
                    flow_pair
                )

        # Bootstrap controller flow discovery when no learned flows
        # are available yet. Generate unique host pairs dynamically
        # from the active Mininet topology.
        if not traffic_flows:

            logger.info(
                "No controller-discovered flows yet; "
                "starting lightweight flow discovery probes"
            )

            for source_index, flow_source in enumerate(
                available_hosts
            ):

                for flow_destination in available_hosts[
                    source_index + 1:
                ]:

                    traffic_flows.append(
                        (
                            flow_source,
                            flow_destination,
                        )
                    )

            # A complete pair matrix can become unnecessarily large
            # on big topologies. Keep discovery bounded.
            traffic_flows = traffic_flows[:8]

            for flow_index, (
                flow_source,
                flow_destination,
            ) in enumerate(
                traffic_flows,
                start=1
            ):

                logger.info(
                    f"Flow discovery probe {flow_index}: "
                    f"{flow_source.name}->"
                    f"{flow_destination.name}"
                )

                # First probe in both directions so OS-Ken learns
                # both edge-host locations before resolving paths.
                flow_source.cmd(
                    "ping -c 2 -i 0.1 -W 1 "
                    f"{flow_destination.IP()} "
                    "> /tmp/opensdn_discovery_"
                    f"{flow_index}_forward.log 2>&1 &"
                )

                flow_destination.cmd(
                    "ping -c 2 -i 0.1 -W 1 "
                    f"{flow_source.IP()} "
                    "> /tmp/opensdn_discovery_"
                    f"{flow_index}_reverse.log 2>&1 &"
                )

            # Allow PacketIn processing and flow installation.
            time.sleep(2)

            # Refresh controller state after probes.
            stats_path = Path(
                "runtime/controller_stats/osken.json"
            )

            try:

                if stats_path.exists():

                    controller_stats = json.loads(
                        stats_path.read_text()
                    )

                    controller_flow_paths = (
                        controller_stats.get(
                            "flow_paths",
                            {}
                        )
                    )

                    # Replace bootstrap probe pairs with the actual
                    # flows learned by OS-Ken.
                    discovered_flows = []

                    for flow_key in controller_flow_paths:

                        try:
                            source_mac, destination_mac = (
                                flow_key.split("->", 1)
                            )

                        except ValueError:
                            continue

                        flow_source = host_by_mac.get(
                            source_mac.lower()
                        )
                        flow_destination = host_by_mac.get(
                            destination_mac.lower()
                        )

                        if (
                            flow_source is None
                            or flow_destination is None
                            or flow_source == flow_destination
                        ):
                            continue

                        flow_pair = (
                            flow_source,
                            flow_destination,
                        )

                        if flow_pair not in discovered_flows:
                            discovered_flows.append(
                                flow_pair
                            )

                    if discovered_flows:
                        traffic_flows = discovered_flows

                        logger.info(
                            "OS-Ken learned active flows: "
                            + ", ".join(
                                f"{src.name}->{dst.name}"
                                for src, dst in traffic_flows
                            )
                        )

            except (
                OSError,
                json.JSONDecodeError,
            ) as exc:

                logger.warning(
                    f"Unable to refresh controller "
                    f"flow discovery state: {exc}"
                )

        logger.info(
            "Active/discovered traffic flows: "
            + (
                ", ".join(
                    f"{src.name}->{dst.name}"
                    for src, dst in traffic_flows
                )
                if traffic_flows
                else "none"
            )
        )

        # --------------------------------------------------------
        # DATA PLANE / QOS MATRIX
        # --------------------------------------------------------
        # One row per active flow. This structure is independent of
        # topology size and supports multiple QoS parameters.

        qos_matrix = []

        for flow_id, (flow_source, flow_destination) in enumerate(
            traffic_flows,
            start=1
        ):
            qos_matrix.append({
                "flow_id": flow_id,
                "source": flow_source.name,
                "destination": flow_destination.name,
                "source_ip": flow_source.IP(),
                "destination_ip": flow_destination.IP(),
                "rtt": None,
                "jitter": None,
                "packet_loss": None,
                "throughput": None,
                "bandwidth_utilization": None,
                "path": [],
                "qos_score": None,
            })

        logger.info(
            f"QoS matrix initialized with "
            f"{len(qos_matrix)} flows"
        )

        RuntimeState.update(
            active_flows=len(qos_matrix),
            qos_matrix=qos_matrix,
            stage="QoS Matrix Initialized"
        )

        # Start lightweight background traffic for every additional
        # flow. The primary flow below remains the measurement flow,
        # preserving compatibility with the existing metrics pipeline.
        for flow_index, (flow_source, flow_destination) in enumerate(
            traffic_flows[1:],
            start=2
        ):
            logger.info(
                f"Starting concurrent background flow {flow_index}: "
                f"{flow_source.name}->{flow_destination.name}"
            )

            flow_source.cmd(
                "ping -i 0.2 -W 1 "
                f"{flow_destination.IP()} "
                "> /tmp/opensdn_flow_"
                f"{flow_index}.log 2>&1 &"
            )

        # --------------------------------------------------------
        # PER-FLOW DATA PLANE MEASUREMENT
        # --------------------------------------------------------
        # Collect lightweight QoS measurements for every active flow.
        # This keeps the existing primary metrics pipeline unchanged
        # while allowing each matrix row to carry independent data.

        import re

        for flow_index, (flow_source, flow_destination) in enumerate(
            traffic_flows,
            start=1
        ):
            matrix_row = qos_matrix[flow_index - 1]

            try:
                ping_output = flow_source.cmd(
                    "ping -c 5 -i 0.2 "
                    f"{flow_destination.IP()}"
                )

                loss_match = re.search(
                    r"(\d+(?:\.\d+)?)% packet loss",
                    ping_output
                )

                if loss_match:
                    matrix_row["packet_loss"] = float(
                        loss_match.group(1)
                    )

                rtt_match = re.search(
                    r"=\s*[\d.]+/([\d.]+)/([\d.]+)/",
                    ping_output
                )

                if rtt_match:
                    matrix_row["rtt"] = float(
                        rtt_match.group(1)
                    )

                    min_rtt = float(rtt_match.group(1))
                    max_rtt = float(rtt_match.group(2))

                    matrix_row["jitter"] = round(
                        max_rtt - min_rtt,
                        3
                    )

                logger.info(
                    f"Flow {flow_index} measured: "
                    f"{flow_source.name}->{flow_destination.name} | "
                    f"RTT={matrix_row['rtt']} ms, "
                    f"Jitter={matrix_row['jitter']} ms, "
                    f"Loss={matrix_row['packet_loss']}%"
                )

            except Exception as exc:
                logger.warning(
                    f"Per-flow measurement failed for "
                    f"{flow_source.name}->{flow_destination.name}: "
                    f"{exc}"
                )

        # --------------------------------------------------------
        # QOS MATRIX SCORING
        # --------------------------------------------------------
        # Normalize the measured parameters across active flows.
        # A higher score represents better observed QoS.

        measured_rows = [
            row for row in qos_matrix
            if row.get("rtt") is not None
        ]

        if measured_rows:

            max_rtt = max(
                row.get("rtt") or 0
                for row in measured_rows
            ) or 1

            max_jitter = max(
                row.get("jitter") or 0
                for row in measured_rows
            ) or 1

            max_loss = max(
                row.get("packet_loss") or 0
                for row in measured_rows
            ) or 1

            for row in measured_rows:

                rtt_score = 1 - (
                    (row.get("rtt") or 0) / max_rtt
                )

                jitter_score = 1 - (
                    (row.get("jitter") or 0) / max_jitter
                )

                loss_score = 1 - (
                    (row.get("packet_loss") or 0) / max_loss
                )

                # Initial adaptive-ready weighting.
                row["qos_score"] = round(
                    (
                        rtt_score * 0.35
                        + jitter_score * 0.25
                        + loss_score * 0.40
                    ) * 100,
                    2
                )

                logger.info(
                    f"QoS score for flow "
                    f"{row['source']}->{row['destination']}: "
                    f"{row['qos_score']}"
                )

        # --------------------------------------------------------
        # DATA PLANE LINK MATRIX
        # --------------------------------------------------------
        # Build a normalized representation of the deployed links.
        # This describes the reusable data plane independently from
        # individual traffic flows.

        link_matrix = []

        for link_id, link in enumerate(
            inventory.links,
            start=1
        ):
            link_matrix.append({
                "link_id": link_id,
                "source": link.source,
                "destination": link.destination,
                "source_port": link.source_port,
                "destination_port": link.destination_port,
                "bandwidth": link.bandwidth,
                "delay": link.delay,
                "configured_loss": link.loss,
                "utilization": None,
                "observed_loss": None,
                "status": "active",
            })

        logger.info(
            f"Data plane link matrix initialized with "
            f"{len(link_matrix)} links"
        )

        RuntimeState.update(
            qos_matrix=qos_matrix,
            link_matrix=link_matrix,
            active_flows=len(qos_matrix)
        )

        # --------------------------------------------------------
        # DATA PLANE PATH DISCOVERY
        # --------------------------------------------------------
        # Build a switch-level adjacency graph from the reusable
        # link matrix. Host-facing links are excluded from path
        # traversal because paths are selected between switches.

        switch_names = {
            device.hostname
            for device in inventory.devices
            if device.device_type == "switch"
        }

        adjacency = {
            switch_name: set()
            for switch_name in switch_names
        }

        for link_row in link_matrix:

            source = link_row["source"]
            destination = link_row["destination"]

            if (
                source in switch_names
                and destination in switch_names
            ):
                adjacency[source].add(destination)
                adjacency[destination].add(source)

        def discover_paths(
            current,
            target,
            visited=None,
            max_paths=10
        ):
            if visited is None:
                visited = []

            visited = visited + [current]

            if current == target:
                return [visited]

            paths = []

            for neighbor in adjacency.get(current, []):

                if neighbor in visited:
                    continue

                for candidate in discover_paths(
                    neighbor,
                    target,
                    visited,
                    max_paths
                ):
                    paths.append(candidate)

                    if len(paths) >= max_paths:
                        return paths

            return paths

        # Find the switch connected to each host.
        host_switch = {}

        for link_row in link_matrix:

            source = link_row["source"]
            destination = link_row["destination"]

            if source in switch_names:
                if destination not in switch_names:
                    host_switch[destination] = source

            elif destination in switch_names:
                if source not in switch_names:
                    host_switch[source] = destination

        # Attach candidate paths to every active flow.
        for flow_row in qos_matrix:

            ingress_switch = host_switch.get(
                flow_row["source"]
            )

            egress_switch = host_switch.get(
                flow_row["destination"]
            )

            candidate_paths = []

            if ingress_switch and egress_switch:

                candidate_paths = discover_paths(
                    ingress_switch,
                    egress_switch
                )

            flow_row["path"] = candidate_paths

            logger.info(
                f"Candidate paths for "
                f"{flow_row['source']}->{flow_row['destination']}: "
                f"{candidate_paths}"
            )

        # --------------------------------------------------------
        # PATH QOS MATRIX
        # --------------------------------------------------------
        # Expand every flow into one row per candidate path.
        # Link-level parameters are aggregated for each path so that
        # the QoS engine can compare candidate routes.

        path_qos_matrix = []

        link_lookup = {}

        for link_row in link_matrix:

            source = link_row["source"]
            destination = link_row["destination"]

            link_lookup[
                (source, destination)
            ] = link_row

            link_lookup[
                (destination, source)
            ] = link_row

        path_id = 1

        for flow_row in qos_matrix:

            candidate_paths = flow_row.get("path") or []

            for candidate_path in candidate_paths:

                path_links = []

                for index in range(
                    len(candidate_path) - 1
                ):
                    link_key = (
                        candidate_path[index],
                        candidate_path[index + 1]
                    )

                    link_row = link_lookup.get(link_key)

                    if link_row:
                        path_links.append(link_row)

                bandwidth_values = []

                for link in path_links:
                    value = link.get("bandwidth")

                    if value is None:
                        continue

                    try:
                        bandwidth_values.append(
                            float(value)
                        )
                    except (
                        TypeError,
                        ValueError,
                    ):
                        logger.warning(
                            f"Invalid bandwidth value ignored: "
                            f"{value!r}"
                        )

                delay_values = []

                for link in path_links:
                    value = link.get("delay")

                    if value is None:
                        continue

                    try:
                        delay_values.append(
                            float(value)
                        )
                    except (
                        TypeError,
                        ValueError,
                    ):
                        logger.warning(
                            f"Invalid delay value ignored: "
                            f"{value!r}"
                        )

                loss_values = []

                for link in path_links:
                    value = link.get("configured_loss")

                    if value is None:
                        continue

                    try:
                        loss_values.append(
                            float(value)
                        )
                    except (
                        TypeError,
                        ValueError,
                    ):
                        logger.warning(
                            f"Invalid configured_loss value ignored: "
                            f"{value!r}"
                        )

                utilization_values = []

                for link in path_links:
                    value = link.get("utilization")

                    if value is None:
                        continue

                    try:
                        utilization_values.append(
                            float(value)
                        )
                    except (
                        TypeError,
                        ValueError,
                    ):
                        logger.warning(
                            f"Invalid utilization value ignored: "
                            f"{value!r}"
                        )

                path_qos_matrix.append({
                    "path_id": path_id,
                    "flow_id": flow_row["flow_id"],
                    "source": flow_row["source"],
                    "destination": flow_row["destination"],
                    "path": candidate_path,
                    "hop_count": len(candidate_path) - 1,

                    # Flow-level observed QoS.
                    "rtt": flow_row.get("rtt"),
                    "jitter": flow_row.get("jitter"),
                    "packet_loss": flow_row.get(
                        "packet_loss"
                    ),
                    "throughput": flow_row.get(
                        "throughput"
                    ),

                    # Path-level aggregated QoS.
                    # Available bandwidth is limited by the weakest link.
                    "available_bandwidth": (
                        min(bandwidth_values)
                        if bandwidth_values
                        else None
                    ),

                    # End-to-end delay is additive.
                    "configured_delay": (
                        sum(delay_values)
                        if delay_values
                        else None
                    ),

                    # Loss and utilization are initially represented
                    # as averages until live per-link measurements
                    # are connected.
                    "configured_loss": (
                        sum(loss_values) / len(loss_values)
                        if loss_values
                        else None
                    ),

                    "average_utilization": (
                        sum(utilization_values)
                        / len(utilization_values)
                        if utilization_values
                        else None
                    ),

                    "path_qos_score": None,
                })

                path_id += 1

        logger.info(
            f"Path QoS matrix initialized with "
            f"{len(path_qos_matrix)} candidate paths"
        )

        # --------------------------------------------------------
        # PATH QOS SCORING AND BEST PATH SELECTION
        # --------------------------------------------------------
        # Compare candidate paths independently for each flow.
        # Lower delay, loss, utilization and hop count are preferred.
        # Higher available bandwidth is preferred.

        selected_paths = {}

        if path_qos_matrix:

            max_delay = max(
                row.get("configured_delay") or 0
                for row in path_qos_matrix
            ) or 1

            max_loss = max(
                row.get("configured_loss") or 0
                for row in path_qos_matrix
            ) or 1

            max_utilization = max(
                row.get("average_utilization") or 0
                for row in path_qos_matrix
            ) or 1

            max_hops = max(
                row.get("hop_count") or 0
                for row in path_qos_matrix
            ) or 1

            max_bandwidth = max(
                row.get("available_bandwidth") or 0
                for row in path_qos_matrix
            ) or 1

            for row in path_qos_matrix:

                delay_score = 1 - (
                    (row.get("configured_delay") or 0)
                    / max_delay
                )

                loss_score = 1 - (
                    (row.get("configured_loss") or 0)
                    / max_loss
                )

                utilization_score = 1 - (
                    (row.get("average_utilization") or 0)
                    / max_utilization
                )

                hop_score = 1 - (
                    (row.get("hop_count") or 0)
                    / max_hops
                )

                bandwidth_score = (
                    (row.get("available_bandwidth") or 0)
                    / max_bandwidth
                )

                row["path_qos_score"] = round(
                    (
                        delay_score * 0.25
                        + loss_score * 0.25
                        + bandwidth_score * 0.25
                        + utilization_score * 0.15
                        + hop_score * 0.10
                    ) * 100,
                    2
                )

            # Select the highest-scoring candidate for every flow.
            for row in path_qos_matrix:

                flow_id = row["flow_id"]

                current_best = selected_paths.get(flow_id)

                if (
                    current_best is None
                    or row["path_qos_score"]
                    > current_best["path_qos_score"]
                ):
                    selected_paths[flow_id] = row

            # Attach the selected path back to the flow matrix.
            for flow_row in qos_matrix:

                selected = selected_paths.get(
                    flow_row["flow_id"]
                )

                if selected:

                    flow_row["selected_path"] = (
                        selected["path"]
                    )

                    flow_row["selected_path_score"] = (
                        selected["path_qos_score"]
                    )

                    logger.info(
                        f"Selected path for "
                        f"{flow_row['source']}->"
                        f"{flow_row['destination']}: "
                        f"{selected['path']} "
                        f"(score={selected['path_qos_score']})"
                    )

        # --------------------------------------------------------
        # QOS ORCHESTRATION DECISION
        # --------------------------------------------------------
        # Compare the newly selected path with the path currently
        # active for each flow. A controller action is requested only
        # when a path changes with meaningful QoS improvement.

        if not hasattr(self, "active_flow_paths"):
            self.active_flow_paths = {}

        qos_decisions = []

        minimum_improvement = 5.0

        for flow_row in qos_matrix:

            flow_id = flow_row["flow_id"]

            selected_path = flow_row.get(
                "selected_path"
            )

            selected_score = flow_row.get(
                "selected_path_score"
            )

            previous = self.active_flow_paths.get(
                flow_id
            )

            decision = {
                "flow_id": flow_id,
                "source": flow_row["source"],
                "destination": flow_row["destination"],
                "previous_path": (
                    previous.get("path")
                    if previous else None
                ),
                "selected_path": selected_path,
                "previous_score": (
                    previous.get("score")
                    if previous else None
                ),
                "selected_score": selected_score,
                "action": "KEEP",
                "improvement": 0.0,
            }

            if selected_path and selected_score is not None:

                if previous is None:

                    decision["action"] = "INSTALL"

                    self.active_flow_paths[flow_id] = {
                        "path": selected_path,
                        "score": selected_score,
                    }

                else:

                    previous_score = previous.get(
                        "score"
                    ) or 0.0

                    improvement = (
                        selected_score
                        - previous_score
                    )

                    decision["improvement"] = round(
                        improvement,
                        2
                    )

                    if (
                        selected_path != previous.get("path")
                        and improvement >= minimum_improvement
                    ):

                        decision["action"] = "REROUTE"

                        self.active_flow_paths[flow_id] = {
                            "path": selected_path,
                            "score": selected_score,
                        }

            qos_decisions.append(decision)

            logger.info(
                f"QoS decision for "
                f"{decision['source']}->"
                f"{decision['destination']}: "
                f"{decision['action']} | "
                f"path={decision['selected_path']} | "
                f"improvement={decision['improvement']}"
            )

        # --------------------------------------------------------
        # CONTROLLER COMMAND EXPORT
        # --------------------------------------------------------

        logger.info(
            "Reached QoS controller command export stage"
        )
        # Export only actionable QoS decisions. The existing OS-Ken
        # process consumes this file during its monitoring cycle.

        actionable_decisions = [
            decision
            for decision in qos_decisions
            if decision.get("action") in (
                "INSTALL",
                "REROUTE",
            )
        ]

        command_directory = Path(
            "runtime/controller_commands"
        )

        command_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        command_path = (
            command_directory
            / "qos_decisions.json"
        )

        command_payload = {
            "experiment_id": experiment.experiment_id,
            "decisions": actionable_decisions,
        }

        temp_command_path = (
            command_directory
            / (
                "qos_decisions."
                + str(experiment.experiment_id)
                + ".tmp"
            )
        )

        temp_command_path.write_text(
            json.dumps(
                command_payload,
                indent=4,
                default=str,
            )
        )

        temp_command_path.replace(
            command_path
        )

        logger.info(
            f"Exported {len(actionable_decisions)} "
            f"QoS controller decisions"
        )

        RuntimeState.update(
            qos_matrix=qos_matrix,
            link_matrix=link_matrix,
            path_qos_matrix=path_qos_matrix,
            qos_decisions=qos_decisions,
            stage="QoS Orchestration Decision Ready"
        )

        # Preserve the primary flow variables for the existing
        # measurement/controller/QoS pipeline.
        source_host, destination_host = traffic_flows[0]

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
            "Final run completed. Keeping Mininet topology active "
            "for future GUI experiments."
        )

        # Keep the deployed data plane alive so subsequent GUI
        # experiments can reuse it. Full cleanup is reserved for
        # an explicit reset/stop or a required topology rebuild.

        logger.info(
            "Mininet topology retained for runtime reuse"
        )

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
