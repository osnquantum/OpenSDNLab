"""
OpenSDNLab SDN Controller
Topology-aware shortest-path forwarding using OS-Ken.
"""

from os_ken.base import app_manager
from os_ken.controller import ofp_event
from os_ken.controller.handler import (
    CONFIG_DISPATCHER,
    MAIN_DISPATCHER,
    DEAD_DISPATCHER,
    set_ev_cls,
)
from os_ken.topology import event
from os_ken.topology.api import get_switch, get_link
from os_ken.ofproto import ofproto_v1_3
from os_ken.lib.packet import packet
from os_ken.lib.packet import ethernet
from os_ken.lib import hub

from engine.analysis.link.link_metrics_engine import (
    link_metrics_engine,
)

import json
import os
import time
from collections import deque


class SimpleSwitch13(app_manager.OSKenApp):

    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):

        super(SimpleSwitch13, self).__init__(*args, **kwargs)

        self.datapaths = {}

        # Active datapath IDs currently connected
        self.active_datapaths = set()

        # MAC -> (dpid, port)
        self.host_locations = {}

        # (source_mac, destination_mac) -> actual switch path
        # Path is recorded when the controller resolves and installs
        # forwarding rules for a known destination.
        self.flow_paths = {}

        # dpid -> {neighbor_dpid: out_port}
        self.graph = {}

        # --------------------------------------------------
        # TOPOLOGY LINK MAP
        # --------------------------------------------------
        #
        # Stores exact OpenFlow link endpoints.
        #
        # Example:
        #
        # (1, 2) -> {
        #     "src_dpid": 1,
        #     "src_port": 2,
        #     "dst_dpid": 2,
        #     "dst_port": 1
        # }
        #
        # The forwarding graph remains unchanged.
        # This structure is used for dynamic link metrics.
        self.link_map = {}

        # Latest calculated logical link metrics
        self.link_metrics = {}

        self.stats = {
            "switch_count": 0,
            "packet_in_count": 0,
            "flow_install_count": 0,
            "topology_switch_count": 0,
            "topology_link_count": 0,
        }

        # --------------------------------------------------
        # DYNAMIC OPENFLOW PORT MONITORING
        # --------------------------------------------------

        # Previous raw counters:
        # (dpid, port_no) -> counter snapshot
        self.port_counters = {}

        # Latest calculated dynamic port metrics
        self.port_metrics = {}

        # Monitoring interval in seconds
        self.monitor_interval = 2

        # Start OpenFlow statistics monitor
        self.monitor_thread = hub.spawn(
            self._monitor_ports
        )

    def export_stats(self):

        self.stats["active_datapaths"] = sorted(
            self.active_datapaths
        )

        # Export controller-resolved forwarding paths.
        # JSON requires string keys, so each MAC flow is represented
        # as "source_mac->destination_mac".
        self.stats["flow_paths"] = {
            f"{source}->{destination}": list(flow_path)
            for (source, destination), flow_path
            in self.flow_paths.items()
        }

        path = "runtime/controller_stats/osken.json"

        os.makedirs(
            "runtime/controller_stats",
            exist_ok=True,
        )

        temp_path = (
            path
            + "."
            + str(os.getpid())
            + "."
            + str(time.time_ns())
            + ".tmp"
        )

        with open(temp_path, "w") as f:
            json.dump(
                self.stats,
                f,
                indent=4,
            )

        os.replace(
            temp_path,
            path,
        )

    ############################################################
    # DYNAMIC OPENFLOW PORT MONITORING
    ############################################################

    def _monitor_ports(self):

        while True:

            for datapath in list(
                self.datapaths.values()
            ):

                self._request_port_stats(
                    datapath
                )

            hub.sleep(
                self.monitor_interval
            )


    def _request_port_stats(
        self,
        datapath
    ):

        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        request = (
            parser.OFPPortStatsRequest(
                datapath,
                0,
                ofproto.OFPP_ANY
            )
        )

        datapath.send_msg(
            request
        )


    @set_ev_cls(
        ofp_event.EventOFPPortStatsReply,
        MAIN_DISPATCHER,
    )
    def port_stats_reply_handler(
        self,
        ev
    ):

        datapath = ev.msg.datapath
        dpid = datapath.id

        current_time = time.time()

        for stat in ev.msg.body:

            port_no = stat.port_no

            # Ignore OpenFlow reserved ports.
            if port_no > datapath.ofproto.OFPP_MAX:
                continue

            key = (
                dpid,
                port_no
            )

            current = {

                "timestamp":
                    current_time,

                "tx_bytes":
                    stat.tx_bytes,

                "rx_bytes":
                    stat.rx_bytes,

                "tx_packets":
                    stat.tx_packets,

                "rx_packets":
                    stat.rx_packets,

                "tx_errors":
                    stat.tx_errors,

                "rx_errors":
                    stat.rx_errors,
            }

            previous = self.port_counters.get(
                key
            )

            self.port_counters[key] = (
                current
            )

            # First sample only establishes
            # the counter baseline.
            if previous is None:
                continue

            elapsed = (
                current_time
                - previous["timestamp"]
            )

            if elapsed <= 0:
                continue

            tx_bytes_delta = max(
                0,
                current["tx_bytes"]
                - previous["tx_bytes"]
            )

            rx_bytes_delta = max(
                0,
                current["rx_bytes"]
                - previous["rx_bytes"]
            )

            tx_packets_delta = max(
                0,
                current["tx_packets"]
                - previous["tx_packets"]
            )

            rx_packets_delta = max(
                0,
                current["rx_packets"]
                - previous["rx_packets"]
            )

            tx_errors_delta = max(
                0,
                current["tx_errors"]
                - previous["tx_errors"]
            )

            rx_errors_delta = max(
                0,
                current["rx_errors"]
                - previous["rx_errors"]
            )

            total_bytes_delta = (
                tx_bytes_delta
                + rx_bytes_delta
            )

            total_packets_delta = (
                tx_packets_delta
                + rx_packets_delta
            )

            throughput_mbps = (
                total_bytes_delta
                * 8
                / elapsed
                / 1_000_000
            )

            packet_rate = (
                total_packets_delta
                / elapsed
            )

            self.port_metrics[
                key
            ] = {

                "dpid":
                    dpid,

                "port_no":
                    port_no,

                "timestamp":
                    current_time,

                "interval_seconds":
                    round(elapsed, 4),

                "throughput_mbps":
                    round(
                        throughput_mbps,
                        4
                    ),

                "packet_rate":
                    round(
                        packet_rate,
                        4
                    ),

                "tx_bytes_delta":
                    tx_bytes_delta,

                "rx_bytes_delta":
                    rx_bytes_delta,

                "tx_packets_delta":
                    tx_packets_delta,

                "rx_packets_delta":
                    rx_packets_delta,

                "tx_errors_delta":
                    tx_errors_delta,

                "rx_errors_delta":
                    rx_errors_delta,

                "tx_bytes":
                    current["tx_bytes"],

                "rx_bytes":
                    current["rx_bytes"],

                "tx_packets":
                    current["tx_packets"],

                "rx_packets":
                    current["rx_packets"],

                "tx_errors":
                    current["tx_errors"],

                "rx_errors":
                    current["rx_errors"],
            }

        self._update_port_statistics()

        self._rebuild_link_metrics()


    def _rebuild_link_metrics(
        self
    ):

        self.link_metrics = (
            link_metrics_engine.build(
                link_map=self.link_map,
                port_metrics=self.port_metrics,
            )
        )

        self._update_link_statistics()


    def _update_port_statistics(
        self
    ):

        ports = {}

        for key, metrics in (
            self.port_metrics.items()
        ):

            dpid, port_no = key

            switch_ports = ports.setdefault(
                str(dpid),
                {}
            )

            # Remove identifiers already represented
            # by the nested structure.
            exported_metrics = {
                name: value
                for name, value in metrics.items()
                if name not in (
                    "dpid",
                    "port_no"
                )
            }

            switch_ports[
                str(port_no)
            ] = exported_metrics


        self.stats[
            "port_metrics"
        ] = ports

        self.stats[
            "port_metric_count"
        ] = sum(
            len(switch_ports)
            for switch_ports
            in ports.values()
        )

        self.stats[
            "switch_port_metric_count"
        ] = {
            dpid: len(switch_ports)
            for dpid, switch_ports
            in ports.items()
        }

        self.stats[
            "port_monitoring_enabled"
        ] = True

        self.stats[
            "port_monitor_interval"
        ] = self.monitor_interval

        self.export_stats()


    def _update_link_statistics(
        self
    ):

        self.stats[
            "link_metrics"
        ] = self.link_metrics

        self.stats[
            "link_metric_count"
        ] = len(
            self.link_metrics
        )

        self.stats[
            "link_monitoring_enabled"
        ] = True

        self.export_stats()


    ############################################################
    # DATAPATH HEALTH
    ############################################################

    @set_ev_cls(
        ofp_event.EventOFPStateChange,
        [MAIN_DISPATCHER, DEAD_DISPATCHER],
    )
    def datapath_state_change_handler(self, ev):

        datapath = ev.datapath
        dpid = datapath.id

        if ev.state == MAIN_DISPATCHER:

            self.datapaths[dpid] = datapath
            self.active_datapaths.add(dpid)

            self.stats["switch_count"] = len(
                self.active_datapaths
            )

            self.logger.info(
                "Datapath connected: dpid=%s",
                dpid,
            )

            # Give OS-Ken topology discovery time to
            # observe LLDP packets and register links.
            hub.spawn(
                self._delayed_topology_refresh
            )

        elif ev.state == DEAD_DISPATCHER:

            self.datapaths.pop(dpid, None)
            self.active_datapaths.discard(dpid)

            self.stats["switch_count"] = len(
                self.active_datapaths
            )

            self.logger.warning(
                "Datapath disconnected: dpid=%s",
                dpid,
            )

            # Refresh topology after a switch
            # disappears from the active datapath set.
            self.refresh_topology()

        self.export_stats()


    def _delayed_topology_refresh(
        self
    ):

        # Allow LLDP-based topology discovery to complete.
        hub.sleep(
            3
        )

        self.refresh_topology()


    ############################################################
    # TOPOLOGY DISCOVERY
    ############################################################

    def refresh_topology(self):

        switches = get_switch(self, None)
        links = get_link(self, None)

        # OS-Ken topology discovery is asynchronous and may
        # temporarily return a partial topology during events.
        # Do not replace an already more complete topology with
        # a smaller transient discovery result.
        if self.graph and self.link_map:

            current_switches = len(self.graph)
            current_links = len(self.link_map)

            if (
                len(switches) < current_switches
                or len(links) < current_links
            ):
                self.logger.info(
                    "Ignoring transient partial topology: "
                    "switches=%s links=%s "
                    "(current switches=%s links=%s)",
                    len(switches),
                    len(links),
                    current_switches,
                    current_links,
                )
                return

        # Rebuild topology structures from
        # the latest OS-Ken discovery result.
        self.graph = {}
        self.link_map = {}

        for switch in switches:
            self.graph.setdefault(
                switch.dp.id,
                {},
            )

        for link in links:

            src = link.src.dpid
            dst = link.dst.dpid

            src_port = link.src.port_no
            dst_port = link.dst.port_no

            # --------------------------------------------------
            # FORWARDING GRAPH
            # --------------------------------------------------

            self.graph.setdefault(
                src,
                {},
            )

            self.graph[src][dst] = src_port

            # --------------------------------------------------
            # EXACT LINK ENDPOINT MAP
            # --------------------------------------------------
            #
            # Example:
            #
            # (1, 2) -> {
            #     "src_dpid": 1,
            #     "src_port": 2,
            #     "dst_dpid": 2,
            #     "dst_port": 1
            # }
            #
            # OS-Ken topology discovery normally reports both
            # directions independently. LinkMetricsEngine will
            # later normalize them into one logical link.

            self.link_map[
                (
                    src,
                    src_port,
                )
            ] = {
                "src_dpid": src,
                "src_port": src_port,
                "dst_dpid": dst,
                "dst_port": dst_port,
            }

        self.stats["topology_switch_count"] = len(
            self.graph
        )

        self.stats["topology_link_count"] = len(
            links
        )

        # Rebuild link metrics using the latest
        # discovered topology and available port metrics.
        self._rebuild_link_metrics()

        self.export_stats()

        self.logger.info(
            "Topology updated: switches=%s links=%s",
            len(self.graph),
            len(links),
        )

        self.logger.info(
            "Network graph: %s",
            self.graph,
        )

    @set_ev_cls(event.EventSwitchEnter)
    def switch_enter_handler(self, ev):

        self.logger.info("Switch entered topology")
        self.refresh_topology()

    @set_ev_cls(event.EventSwitchLeave)
    def switch_leave_handler(self, ev):

        self.logger.info("Switch left topology")
        self.refresh_topology()

    @set_ev_cls(event.EventLinkAdd)
    def link_add_handler(self, ev):

        self.logger.info("Link added")
        self.refresh_topology()

    @set_ev_cls(event.EventLinkDelete)
    def link_delete_handler(self, ev):

        self.logger.info("Link deleted")
        self.refresh_topology()

    ############################################################
    # SHORTEST PATH
    ############################################################

    def shortest_path(self, source, destination):

        if source == destination:
            return [source]

        visited = set()
        queue = deque([(source, [source])])

        while queue:

            current, path = queue.popleft()

            if current == destination:
                return path

            if current in visited:
                continue

            visited.add(current)

            for neighbor in self.graph.get(current, {}):

                if neighbor not in visited:
                    queue.append(
                        (
                            neighbor,
                            path + [neighbor],
                        )
                    )

        return None

    ############################################################
    # ADAPTIVE PATH RECOVERY
    ############################################################

    def apply_recovery_path(
        self,
        path,
        destination=None,
        priority=100,
    ):

        if not path or len(path) < 2:

            return {
                "executed": False,
                "success": False,
                "reason": "Recovery path is too short",
            }

        def resolve_switch(node):

            if isinstance(node, int):
                return node

            if isinstance(node, str):
                name = node.strip()

                if name.startswith("s") and name[1:].isdigit():
                    return int(name[1:])

            return None


        switch_path = [
            resolved
            for node in path
            for resolved in [resolve_switch(node)]
            if resolved is not None
        ]

        if len(switch_path) < 2:

            return {
                "executed": False,
                "success": False,
                "reason":
                    "Recovery path does not contain "
                    "enough switches",
                "path": path,
                "switch_path": switch_path,
            }

        installed_switches = []

        destination_mac = None
        destination_location = None

        if destination is not None:

            if destination in self.host_locations:

                destination_mac = destination
                destination_location = (
                    self.host_locations[destination]
                )

            else:

                destination_name = str(
                    destination
                ).lower()

                for mac, location in (
                    self.host_locations.items()
                ):

                    mac_suffix = mac.split(
                        ":"
                    )[-1].lower()

                    if (
                        destination_name.startswith("h")
                        and destination_name[1:].isdigit()
                        and int(destination_name[1:])
                        == int(mac_suffix, 16)
                    ):

                        destination_mac = mac
                        destination_location = location
                        break

        if destination_location is None:

            return {
                "executed": False,
                "success": False,
                "reason":
                    "Destination host location unavailable",
                "path": path,
                "switch_path": switch_path,
                "destination": destination,
            }

        destination_dpid, destination_port = (
            destination_location
        )

        if switch_path[-1] != destination_dpid:

            return {
                "executed": False,
                "success": False,
                "reason":
                    "Recovery path does not end at "
                    "destination switch",
                "path": path,
                "switch_path": switch_path,
                "destination_dpid": destination_dpid,
            }

        for index, switch_id in enumerate(switch_path):

            datapath = self.datapaths.get(
                switch_id
            )

            if datapath is None:

                return {
                    "executed": False,
                    "success": False,
                    "reason":
                        f"Datapath unavailable for switch "
                        f"{switch_id}",
                    "installed_switches":
                        installed_switches,
                }

            if index == len(switch_path) - 1:

                out_port = destination_port

            else:

                next_switch = switch_path[index + 1]

                out_port = self.graph.get(
                    switch_id,
                    {},
                ).get(
                    next_switch
                )

                if out_port is None:

                    return {
                        "executed": False,
                        "success": False,
                        "reason":
                            f"No link from {switch_id} "
                            f"to {next_switch}",
                        "installed_switches":
                            installed_switches,
                    }

            parser = datapath.ofproto_parser

            match_kwargs = {}

            if destination_mac is not None:
                match_kwargs["eth_dst"] = destination_mac

            match = parser.OFPMatch(
                **match_kwargs
            )

            actions = [
                parser.OFPActionOutput(
                    out_port
                )
            ]

            self.add_flow(
                datapath,
                priority,
                match,
                actions,
            )

            installed_switches.append(
                switch_id
            )


        return {
            "executed": True,
            "success": True,
            "path": path,
            "switch_path": switch_path,
            "destination": destination,
            "destination_dpid": destination_dpid,
            "installed_switches":
                installed_switches,
            "priority": priority,
        }


    ############################################################
    # FLOW INSTALLATION
    ############################################################

    def add_flow(
        self,
        datapath,
        priority,
        match,
        actions,
    ):

        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        instructions = [
            parser.OFPInstructionActions(
                ofproto.OFPIT_APPLY_ACTIONS,
                actions,
            )
        ]

        flow_mod = parser.OFPFlowMod(
            datapath=datapath,
            priority=priority,
            match=match,
            instructions=instructions,
        )

        datapath.send_msg(flow_mod)

        self.stats["flow_install_count"] += 1
        self.export_stats()

    ############################################################
    # SWITCH CONNECTION
    ############################################################

    @set_ev_cls(
        ofp_event.EventOFPSwitchFeatures,
        CONFIG_DISPATCHER,
    )
    def switch_features_handler(self, ev):

        datapath = ev.msg.datapath

        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        match = parser.OFPMatch()

        actions = [
            parser.OFPActionOutput(
                ofproto.OFPP_CONTROLLER,
                ofproto.OFPCML_NO_BUFFER,
            )
        ]

        self.add_flow(
            datapath,
            0,
            match,
            actions,
        )

        self.logger.info(
            "Switch connected: %s",
            datapath.id,
        )

    ############################################################
    # PACKET PROCESSING
    ############################################################

    @set_ev_cls(
        ofp_event.EventOFPPacketIn,
        MAIN_DISPATCHER,
    )
    def packet_in_handler(self, ev):

        self.stats["packet_in_count"] += 1

        msg = ev.msg
        datapath = msg.datapath

        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        dpid = datapath.id
        in_port = msg.match["in_port"]

        pkt = packet.Packet(msg.data)

        eth = pkt.get_protocol(
            ethernet.ethernet
        )

        if eth is None:
            return

        src = eth.src
        dst = eth.dst

        # Ignore LLDP packets.
        if eth.ethertype == 0x88CC:
            return

        ########################################################
        # LEARN SOURCE HOST LOCATION
        ########################################################

        # Build neighbor ports from the directional topology
        # map rather than only the graph. During asynchronous
        # topology discovery, graph updates may temporarily be
        # incomplete while link_map already contains the physical
        # inter-switch port relationships.
        neighbor_ports = {
            link["src_port"]
            for link in self.link_map.values()
            if link["src_dpid"] == dpid
        }


        # Learn only unicast hosts arriving on edge ports.
        is_multicast = bool(int(src.split(":")[0], 16) & 1)

        if not is_multicast and in_port not in neighbor_ports:

            previous = self.host_locations.get(src)

            if previous is None:

                self.host_locations[src] = (
                    dpid,
                    in_port,
                )

                self.logger.info(
                    "Host learned: %s -> switch=%s port=%s",
                    src,
                    dpid,
                    in_port,
                )

        ########################################################
        # DESTINATION UNKNOWN
        ########################################################

        if dst not in self.host_locations:

            self.logger.info(
                "Unknown destination: %s",
                dst,
            )

            actions = []

            for port_no in datapath.ports:

                if port_no <= 0:
                    continue

                if port_no == in_port:
                    continue

                actions.append(
                    parser.OFPActionOutput(
                        port_no
                    )
                )

            if actions:

                data = None

                if msg.buffer_id == ofproto.OFP_NO_BUFFER:
                    data = msg.data

                out = parser.OFPPacketOut(
                    datapath=datapath,
                    buffer_id=msg.buffer_id,
                    in_port=in_port,
                    actions=actions,
                    data=data,
                )

                datapath.send_msg(out)

            self.export_stats()
            return

        ########################################################
        # DESTINATION KNOWN
        ########################################################

        dst_dpid, dst_port = (
            self.host_locations[dst]
        )

        path = self.shortest_path(
            dpid,
            dst_dpid,
        )

        if not path:

            self.logger.warning(
                "No path from switch %s to %s",
                dpid,
                dst_dpid,
            )

            return

        self.logger.info(
            "Shortest path for %s -> %s: %s",
            src,
            dst,
            path,
        )

        # Record the controller-resolved switch path as the source
        # of truth for this Ethernet flow. The path corresponds to
        # the forwarding rules installed below.
        self.flow_paths[
            (src, dst)
        ] = list(path)

        self.export_stats()

        ########################################################
        # INSTALL PATH FLOWS
        ########################################################

        for index, switch_id in enumerate(path):

            switch_datapath = self.datapaths.get(
                switch_id
            )

            if switch_datapath is None:
                continue

            switch_parser = (
                switch_datapath.ofproto_parser
            )

            if index == len(path) - 1:

                out_port = dst_port

            else:

                next_switch = path[index + 1]

                out_port = self.graph[
                    switch_id
                ][
                    next_switch
                ]

            match = switch_parser.OFPMatch(
                eth_dst=dst
            )

            actions = [
                switch_parser.OFPActionOutput(
                    out_port
                )
            ]

            self.add_flow(
                switch_datapath,
                10,
                match,
                actions,
            )

        ########################################################
        # SEND CURRENT PACKET
        ########################################################

        if len(path) == 1:

            out_port = dst_port

        else:

            out_port = self.graph[
                dpid
            ][
                path[1]
            ]

        actions = [
            parser.OFPActionOutput(
                out_port
            )
        ]

        data = None

        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=msg.buffer_id,
            in_port=in_port,
            actions=actions,
            data=data,
        )

        datapath.send_msg(out)

        self.export_stats()
