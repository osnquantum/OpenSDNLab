
# ============================================================
# ADAPTIVE SDN NETWORK MONITORING, PREDICTION AND RECOVERY
# ============================================================

## Core Research Goal

Develop an adaptive SDN platform capable of:

- Automatically discovering heterogeneous network topology.
- Monitoring the complete reachable network.
- Selecting the minimum useful set of monitoring flows.
- Ensuring reachable links are not silently ignored.
- Detecting QoS degradation.
- Predicting future degradation using GRU.
- Performing adaptive recovery and routing using DRL.
- Handling link failure, host failure and topology changes.

---

## Core Architecture

Network Discovery
        |
        v
Complete Reachable Network Graph
        |
        v
Minimum Flow Coverage Engine
        |
        v
Hybrid Network Monitoring
        |
        v
QoS Metric Collection
        |
        v
Degradation Detection
        |
        v
GRU QoS Prediction
        |
        v
DRL Recovery Decision
        |
        v
SDN Routing / Recovery Action
        |
        v
Post-Recovery Verification

---

## 1. Controller-Independent Topology Discovery

The adaptive framework must not depend on only one SDN controller.

Each controller should expose a common topology interface:

    get_topology()

The standardized topology result should eventually contain:

- switches
- hosts
- links
- ports
- link state
- controller metadata

Possible future controllers:

- OS-Ken
- Ryu
- ONOS
- OpenDaylight
- Floodlight

Each controller adapter translates its own discovery mechanism
into the common OpenSDNLab network representation.

---

## 2. OS-Ken Automatic Discovery

Current OS-Ken controller already starts with:

    --observe-links

Topology discovery is already implemented through:

- get_switch()
- get_link()
- EventSwitchEnter
- EventSwitchLeave
- EventLinkAdd
- EventLinkDelete

Therefore, OpenSDNLab should reuse controller discovery instead
of manually implementing LLDP discovery.

---

## 3. Complete Reachable Network Graph

Combine:

1. Controller-discovered switches.
2. Controller-discovered inter-switch links.
3. Host attachment information.
4. Inventory/topology information.

The result becomes the Complete Reachable Network Graph.

This graph represents all currently reachable network components.

---

## 4. Minimum Flow Coverage Engine

Do not create fixed flows such as:

    h1 -> h2
    h1 -> h3

Instead:

1. Generate candidate host-to-host monitoring flows.
2. Determine the path of each candidate flow.
3. Determine which links each flow covers.
4. Select the flow covering the largest number of uncovered links.
5. Repeat until all reachable links are covered.
6. Minimize unnecessary duplicate monitoring.

Objectives:

- Maximum reachable-link coverage.
- Minimum monitoring flows.
- Reduced measurement overhead.
- No ignored reachable network region.

---

## 5. Hybrid Network Monitoring

Monitoring has two layers.

### Infrastructure Monitoring

Provided by the SDN controller and OpenFlow telemetry:

- switch state
- link state
- port statistics
- packet counters
- byte counters
- errors
- drops
- controller connectivity

### End-to-End QoS Monitoring

Provided by selected monitoring flows:

- RTT
- delay
- jitter
- packet loss
- throughput

The two layers are combined to create a network-wide state.

---

## 6. Host Failure and Monitoring Recovery

A monitoring host must not become a single point of failure.

For each monitoring flow maintain:

- source host
- destination host
- path
- covered links
- alternative monitoring candidates

If a host becomes unavailable:

1. Remove invalid flows.
2. Identify uncovered reachable links.
3. Select replacement monitoring flows.
4. Continue monitoring using available hosts.

Infrastructure telemetry should continue whenever controller
connectivity remains available.

---

## 7. Dynamic Topology Changes

When the controller detects:

- link addition
- link removal
- switch addition
- switch failure
- host connectivity changes

The system should:

1. Refresh topology discovery.
2. Rebuild the reachable graph.
3. Remove invalid monitoring flows.
4. Identify uncovered links.
5. Generate replacement candidates.
6. Recalculate the minimum coverage plan.
7. Continue monitoring.

---

## 8. QoS Degradation Detection

Collect historical network observations including:

- delay
- jitter
- packet loss
- throughput
- RTT
- port statistics
- link utilization
- errors and drops

Each observation contributes to the current network state.

The system must identify:

- stable links
- degrading links
- failed links
- congested paths
- abnormal QoS patterns

---

## 9. GRU-Based QoS Prediction

Use GRU to analyze time-series network metrics.

Input examples:

- recent delay history
- jitter history
- packet loss history
- throughput history
- link utilization
- port statistics

GRU objective:

Predict whether QoS degradation is likely before a serious failure
or SLA violation occurs.

Prediction output becomes part of the adaptive network state.

---

## 10. DRL-Based Recovery

DRL receives the current network state, including:

- discovered topology
- link states
- QoS metrics
- degradation status
- GRU prediction
- available paths
- controller/network constraints

Possible DRL actions:

- keep current route
- reroute traffic
- select alternative path
- avoid degraded link
- adjust monitoring priority
- trigger recovery workflow

Reward should encourage:

- lower delay
- lower packet loss
- lower jitter
- higher throughput
- successful connectivity
- fewer unnecessary route changes

---

## 11. Adaptive Recovery Pipeline

QoS Observation
        |
        v
Degradation Detection
        |
        v
GRU Prediction
        |
        v
DRL Decision
        |
        v
SDN Controller Action
        |
        v
Traffic Rerouting / Recovery
        |
        v
Post-Recovery Measurement
        |
        v
Reward / Learning Feedback

---

# IMPLEMENTATION ROADMAP

## Phase 1 - Controller Topology Interface

[ ] Extend BaseController with get_topology().
[ ] Implement get_topology() for OS-Ken.
[ ] Standardize switches and links into a common format.
[ ] Preserve compatibility with future controllers.

## Phase 2 - Complete Network Discovery

[ ] Retrieve live controller topology.
[ ] Combine controller topology with inventory hosts.
[ ] Build Complete Reachable Network Graph.
[ ] Detect unreachable components.

## Phase 3 - Minimum Flow Coverage Engine

[ ] Generate candidate monitoring flows.
[ ] Discover candidate paths.
[ ] Calculate link coverage for each flow.
[ ] Select minimum useful flow set.
[ ] Track covered and uncovered links.

## Phase 4 - Monitoring Resilience

[ ] Add backup monitoring flows.
[ ] Detect unavailable hosts.
[ ] Replace invalid monitoring flows.
[ ] Recalculate coverage after failures.

## Phase 5 - Hybrid QoS Monitoring

[ ] Collect controller/OpenFlow infrastructure metrics.
[ ] Collect end-to-end QoS metrics.
[ ] Combine metrics into unified network state.
[ ] Store historical observations.

## Phase 6 - Degradation Detection

[ ] Detect abnormal QoS.
[ ] Identify degrading links and paths.
[ ] Create degradation events.
[ ] Connect degradation to affected flows.

## Phase 7 - GRU Prediction

[ ] Prepare historical metric sequences.
[ ] Define GRU input features.
[ ] Train degradation prediction model.
[ ] Integrate predictions into runtime monitoring.

## Phase 8 - DRL Recovery

[ ] Define DRL state.
[ ] Define available recovery actions.
[ ] Define reward function.
[ ] Train recovery policy.
[ ] Connect policy decisions to SDN routing actions.

## Phase 9 - Evaluation

[ ] Normal network.
[ ] Heterogeneous topology.
[ ] Multiple simultaneous flows.
[ ] QoS degradation.
[ ] Congestion.
[ ] Link failure.
[ ] Host failure.
[ ] Dynamic topology change.
[ ] Controller connectivity scenarios.
[ ] Compare reactive recovery with GRU + DRL adaptive recovery.

# CURRENT CHECKPOINT

Current completed work:

[X] Custom topology support.
[X] Asynchronous experiment execution.
[X] Multi-run experiment support.
[X] Reuse deployed Mininet topology between runs.
[X] Existing OS-Ken controller integration.
[X] OS-Ken automatic switch discovery.
[X] OS-Ken automatic link discovery.
[X] Network discovery foundation.

NEXT STEP:

Extend BaseController with:

    get_topology()

Then implement the OS-Ken topology adapter using the topology
already discovered by:

    --observe-links

After that:

Controller Discovery
    ->
Complete Reachable Network Graph
    ->
Minimum Flow Coverage Engine

# ============================================================
# END ADAPTIVE SDN CORE ROADMAP
# ============================================================

