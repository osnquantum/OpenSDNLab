
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


============================================================
PATH RECOVERY STATUS MODEL AND VALIDATION
============================================================


============================================================
DYNAMIC LINK-LEVEL QOS INTELLIGENCE
============================================================

CURRENT STATUS

The OS-Ken controller now dynamically collects OpenFlow
port statistics every monitoring interval.

Currently available dynamic measurements include:

- Throughput
- Packet rate
- TX/RX byte deltas
- TX/RX packet deltas
- TX/RX error deltas
- Raw OpenFlow port counters

The controller remains measurement-driven.

No static QoS degradation thresholds should be embedded
inside the OS-Ken controller.

------------------------------------------------------------
CURRENT ARCHITECTURE PROBLEM
------------------------------------------------------------

OpenFlow statistics are collected per switch port.

However, SDN routing and recovery operate on:

- Links
- Paths
- End-to-end network conditions

A physical bidirectional connection currently produces
two directional port measurements.

Example:

s1:port2 <----------> s2:port1

Current port-level representation:

(1,2) -> s1 to s2
(2,1) -> s2 to s1

These must be normalized into one logical link.

------------------------------------------------------------
NEXT CORE STAGE
LINK METRICS ENGINE
------------------------------------------------------------

Build a topology-aware Link Metrics Engine.

Responsibilities:

1. Read dynamic OpenFlow port metrics.
2. Read SDN topology relationships.
3. Map switch ports to neighboring switches.
4. Combine bidirectional port measurements.
5. Maintain one normalized record per SDN link.
6. Continuously update link metrics.
7. Prevent duplicate link entries.

------------------------------------------------------------
NORMALIZED LINK MODEL
------------------------------------------------------------

Each logical connection should have one link identity.

Example:

link_id:
s1:2--s2:1

Structure:

Link
|
+-- link_id
|
+-- endpoints
|   +-- source_switch
|   +-- source_port
|   +-- destination_switch
|   +-- destination_port
|
+-- forward_metrics
|   +-- throughput
|   +-- packet_rate
|   +-- errors
|
+-- reverse_metrics
|   +-- throughput
|   +-- packet_rate
|   +-- errors
|
+-- aggregated_metrics
    +-- utilization
    +-- congestion_score
    +-- packet_loss_estimate
    +-- error_rate
    +-- link_health

------------------------------------------------------------
LINK METRICS MATRIX
------------------------------------------------------------

For efficient topology-wide lookup, maintain a link matrix.

Example:

            s1        s2        s3

s1           -      LINK01    LINK02
s2        LINK01       -      LINK03
s3        LINK02    LINK03       -

The matrix provides efficient lookup for:

- Link existence
- Neighbor relationships
- Current link metrics
- Path construction
- Path QoS aggregation
- Recovery path selection

------------------------------------------------------------
DYNAMIC LINK HEALTH
------------------------------------------------------------

The controller provides measurements.

The analysis layer interprets measurements.

Dynamic link analysis should calculate:

- Throughput
- Packet rate
- Error rate
- Estimated packet loss
- Utilization
- Congestion score
- Link health

Link health states:

NORMAL
DEGRADED
CRITICAL

Threshold interpretation must remain configurable and
independent from OpenFlow collection.

------------------------------------------------------------
TARGET ARCHITECTURE
------------------------------------------------------------

OpenFlow Switches
        |
        v
OS-Ken Controller
        |
        +--> Port Statistics Collection
        |
        v
Dynamic Port Metrics
        |
        +--> Topology Discovery
        |
        v
Link Metrics Engine
        |
        +--> Bidirectional Link Mapping
        |
        +--> Link Metrics Matrix
        |
        +--> Aggregated Link Metrics
        |
        v
QoS Analysis Layer
        |
        +--> QoS Degradation Engine
        |
        +--> QoS/QoE Analysis
        |
        v
Adaptive Trigger
        |
        v
Decision Engine
        |
        v
Path Recovery / Path Selection
        |
        v
Dashboard

------------------------------------------------------------
DEVELOPMENT SEQUENCE
------------------------------------------------------------

STAGE 1
Build Link Metrics Engine.

STAGE 2
Normalize bidirectional OpenFlow port statistics into
single logical SDN links.

STAGE 3
Build topology-wide Link Metrics Matrix.

STAGE 4
Calculate dynamic link health and QoS indicators.

STAGE 5
Aggregate link metrics into path-level QoS metrics.

STAGE 6
Use measured path conditions for dynamic path selection.

STAGE 7
Connect adaptive recovery to real-time link and path QoS.

STAGE 8
Store historical link and path measurements.

STAGE 9
Expose all dynamic states in the dashboard:

- Controller status
- Port metrics
- Link metrics
- Link health
- Link matrix
- Path metrics
- QoS degradation
- Adaptive decisions
- Recovery status

------------------------------------------------------------
CORE DESIGN PRINCIPLE
------------------------------------------------------------

OpenFlow collects measurements.

Topology identifies relationships.

Link Metrics Engine normalizes connections.

QoS Engine interprets network quality.

Adaptive Engine determines whether action is required.

Recovery Engine selects an improved path.

The SDN controller remains measurement-driven and does
not contain static QoS degradation thresholds.


Date: 2026-08-23

The adaptive recovery framework currently implements PATH_RECOVERY
as the registered recovery strategy.

The Path Recovery workflow is:

QoS Monitoring
        |
        v
QoS Degradation Detection
        |
        v
Adaptive Trigger
        |
        v
REACTIVE_RECOVERY / PROACTIVE_RECOVERY
        |
        v
PATH_RECOVERY
        |
        v
Topology Path Analysis
        |
        v
Alternative Path Discovery
        |
        +-------------------------------+
        |                               |
        v                               v
Alternative Path Available        No Alternative Path
        |                               |
        v                               v
Path Selection                 PATH_RECOVERY_NO_ALTERNATIVE_PATH
        |
        v
PATH_SELECTED
        |
        v
Path Reconfiguration
        |
        +-------------------+
        |                   |
        v                   v
PATH_RECOVERY_EXECUTED   PATH_RECOVERY_FAILED


PATH RECOVERY STATUS DEFINITIONS
------------------------------------------------------------

1. PATH_RECOVERY_DISABLED

Meaning:
Path Recovery is disabled for the experiment.

Condition:
recovery_enabled = false


2. PATH_RECOVERY_NOT_REQUIRED

Meaning:
No QoS degradation requiring Path Recovery was detected.

Condition:
Adaptive trigger was not activated.


3. PATH_RECOVERY_TRIGGERED

Meaning:
QoS degradation was detected and Path Recovery was requested.

Condition:
Adaptive trigger generated a recovery action.


4. PATH_SELECTED

Meaning:
One or more alternative network paths were available and the
PathSelector selected the best recovery path according to path
health, QoS conditions, hop count, and recovery objective.

Condition:
Alternative path analysis succeeded and best_path was selected.


5. PATH_RECOVERY_EXECUTED

Meaning:
The selected alternative path was successfully applied to the
network/controller.

Condition:
Path reconfiguration completed successfully.


6. PATH_RECOVERY_NO_ALTERNATIVE_PATH

Meaning:
QoS degradation triggered Path Recovery, but topology analysis found
no alternative path between the source and destination.

This is NOT a software failure.

Example:

h1 -> s1 -> s2 -> s3 -> s4 -> s5 -> h10

If this is the only available path, recovery cannot reroute traffic.

Condition:

alternative_path_available = false


7. PATH_RECOVERY_FAILED

Meaning:
An actual error occurred during Path Recovery processing or path
reconfiguration.

Examples:

- Path analysis error
- Path selection error
- Controller programming failure
- Flow installation failure
- Network reconfiguration failure


VALIDATION COMPLETED
------------------------------------------------------------

Experiment:

EXP-20260808-1e3d7f

Experiment Name:

QoS Analysis


Adaptive Configuration:

prediction_enabled = false
recovery_enabled = true
adaptive_mode = REACTIVE


Observed QoS Metrics:

average_rtt = 123.89 ms
jitter = 174.125 ms
maximum_rtt = 471.095 ms
minimum_rtt = 19.562 ms
one_way_delay = 61.945 ms
packet_loss = 0.0 %
throughput = 50.6
mos = 4.4


Adaptive Decision:

Action:
STABILIZE_TRAFFIC

Reason:
High jitter detected


Adaptive Trigger:

triggered = true
trigger_source = CURRENT_QOS
action = REACTIVE_RECOVERY


Path Analysis Result:

source = h1
destination = h10
path_count = 1
alternative_path_available = false


Detected Path:

h1 -> s1 -> s2 -> s3 -> s4 -> s5 -> h10


Validation Conclusion:

The complete adaptive Path Recovery pipeline was successfully
triggered and executed through topology analysis.

The recovery process correctly determined that the topology contained
only one available path. Therefore, the appropriate semantic result is:

PATH_RECOVERY_NO_ALTERNATIVE_PATH

This result represents a topology limitation rather than a Path
Recovery software failure.


NEXT IMPLEMENTATION STEPS
------------------------------------------------------------

[ ] Replace the current status:

    PATH_RECOVERY_FAILED

when the reason is:

    No alternative path available

with:

    PATH_RECOVERY_NO_ALTERNATIVE_PATH


[ ] Preserve PATH_RECOVERY_FAILED only for genuine execution errors.


[ ] Update dashboard status labels to display:

    Disabled
    Not Required
    Triggered
    Best Path Selected
    Recovery Executed
    No Alternative Path
    Recovery Failed


[ ] Create a redundant custom topology containing at least two
    source-to-destination paths.


[ ] Validate PathSelector using different path health and QoS
    conditions.


[ ] Validate the PATH_SELECTED state.


[ ] Implement controller/network path reconfiguration.


[ ] Validate the PATH_RECOVERY_EXECUTED state.


TARGET REDUNDANT TOPOLOGY
------------------------------------------------------------

                 s2
                /  \
               /    \
h1 ---- s1 ---        --- s4 ---- h2
               \    /
                \  /
                 s3


Primary Path:

h1 -> s1 -> s2 -> s4 -> h2


Alternative Path:

h1 -> s1 -> s3 -> s4 -> h2


Expected Recovery Flow:

QoS Degradation
        |
        v
PATH_RECOVERY_TRIGGERED
        |
        v
Topology Path Analysis
        |
        v
Multiple Paths Available
        |
        v
PathSelector
        |
        v
PATH_SELECTED
        |
        v
Controller Path Reconfiguration
        |
        v
PATH_RECOVERY_EXECUTED


DOCUMENTATION STATUS
------------------------------------------------------------

Path Recovery architecture:
IMPLEMENTED

RecoveryManager registration:
VALIDATED

PathSelector:
VALIDATED

Adaptive Trigger integration:
VALIDATED

Dashboard live API integration:
VALIDATED

Single-path topology handling:
VALIDATED

No alternative path semantic status:
DOCUMENTED - IMPLEMENTATION PENDING

Redundant topology validation:
PENDING

Actual path reconfiguration:
PENDING

PATH_RECOVERY_EXECUTED validation:
PENDING

============================================================

## Core SDN Forwarding — Completed

**Status:** Completed and verified

### Implemented Core Functions

- OS-Ken controller running on OpenFlow port `6653`.
- Mininet topology successfully connected to the external controller.
- OpenFlow 1.3 enabled on Mininet switches.
- Verified topology:

  h1 -- s1 -- s2 -- h2

- Controller learns source host MAC addresses and switch/port locations.
- Unknown destinations are forwarded for host discovery.
- Bidirectional host communication established.
- Forwarding paths are calculated between learned hosts.
- Destination-specific OpenFlow flow rules are installed on both switches.
- ARP resolution verified between `h1` and `h2`.
- Flow-table packet counters confirm installed rules actively forward traffic.

### Verification Results

- h1 -> h2: 3/3 packets received, 0% packet loss.
- h2 -> h1: 3/3 packets received, 0% packet loss.
- Subsequent packets achieved low latency after flow installation.
- Bidirectional OpenFlow rules were verified on both `s1` and `s2`.

### Core Forwarding Pipeline

Packet-In
-> Source MAC Learning
-> Host Location Detection
-> Destination Lookup
-> Shortest Path Calculation
-> OpenFlow Flow Installation
-> Direct Switch Forwarding

### Remaining Core Work

- Verify live topology statistics while both switches remain connected.
- Ensure `switch_count`, `topology_switch_count`, and `active_datapaths` reflect all active switches.
- Fix persistent inter-switch `link_metrics` collection.
- Verify `topology_link_count` and `link_metric_count`.
- Integrate verified link metrics into adaptive QoS path selection.


============================================================
PATH RECOVERY AND REDUNDANT TOPOLOGY
============================================================

Alternative Path:

h1 -> s1 -> s3 -> s4 -> h2


Expected Recovery Flow:

QoS Degradation
        |
        v
PATH_RECOVERY_TRIGGERED
        |
        v
Topology Path Analysis
        |
        v
Multiple Paths Available
        |
        v
PathSelector
        |
        v
PATH_SELECTED
        |
        v
Controller Path Reconfiguration
        |
        v
PATH_RECOVERY_EXECUTED


DOCUMENTATION STATUS
------------------------------------------------------------

Path Recovery architecture:
IMPLEMENTED

RecoveryManager registration:
VALIDATED

PathSelector:
VALIDATED

Adaptive Trigger integration:
VALIDATED

Dashboard live API integration:
VALIDATED

Single-path topology handling:
VALIDATED

No alternative path semantic status:
DOCUMENTED - IMPLEMENTATION PENDING

Redundant topology validation:
PENDING

Actual path reconfiguration:
PENDING

PATH_RECOVERY_EXECUTED validation:
PENDING

============================================================

# Core Requirement: Evidence-Based Composite QoS Quality Score

## Requirement

The Adaptive SDN QoS Framework shall not use arbitrary QoS quality
values, thresholds, normalization bounds, or metric weights.

QoS quality shall be represented using a formally defined Composite
QoS Quality Score (CQQS):

CQQS ∈ [0,100]

QoS_score =
wT * T_score +
wD * D_score +
wJ * J_score +
wL * L_score

Where:

- T = throughput
- D = delay
- J = jitter
- L = packet loss
- w = documented and justified metric weights

## Metric Normalization

All QoS metrics shall be normalized to a common 0–100 scale before
aggregation.

Throughput (higher is better):

T_score = 100 * (T - T_min) / (T_max - T_min)

Delay (lower is better):

D_score = 100 * (D_max - D) / (D_max - D_min)

Jitter (lower is better):

J_score = 100 * (J_max - J) / (J_max - J_min)

Packet loss (lower is better):

L_score = 100 * (L_max - L) / (L_max - L_min)

All normalized metric scores shall be clamped to [0,100].

## Evidence Requirement

The framework shall not hard-code the following values unless they are
supported and documented:

- T_min
- T_max
- D_min
- D_max
- J_min
- J_max
- L_min
- L_max
- wT
- wD
- wJ
- wL

Each value must be justified using one or more of:

1. Recognized standards or recommendations
2. Application-specific QoS requirements
3. Peer-reviewed research
4. Experimentally derived baseline calibration

## Methodological Basis

The composite QoS methodology follows a normalization and weighted
composite-index approach consistent with ITU-T E.813.

SDN research also supports combining normalized QoS metrics for
network decision-making. Specific weights from research papers must
not automatically be adopted unless justified for the corresponding
traffic scenario or experimental design.

## Architecture Requirement

Live Network Metrics
        |
        v
Metric Normalization
        |
        +-- Throughput  -> 0–100
        +-- Delay       -> 0–100
        +-- Jitter      -> 0–100
        +-- Packet Loss -> 0–100
        |
        v
Composite QoS Quality Score
CQQS ∈ [0,100]
        |
        v
QoS Decision Engine
        |
        v
QoS-Aware Routing

## Implementation Constraint

The framework may implement the normalization and composite-score
architecture before final parameter values are selected.

Any provisional thresholds, bounds, or weights used during software
testing must be explicitly labeled:

TEST / PLACEHOLDER ONLY
NOT VALIDATED FOR RESEARCH RESULTS

Placeholder values shall not be presented as scientifically valid QoS
thresholds and shall not be used for final experimental evaluation.

## Next Research Requirement

Before finalizing the CQQS implementation, defensible normalization
bounds and weighting strategies must be identified for:

1. Throughput
2. End-to-end delay
3. Jitter
4. Packet loss

The selected values must be appropriate for the traffic or application
scenario evaluated by the Adaptive SDN QoS Framework.

Current status:
QoS scoring methodology is defined.
Final numerical bounds and metric weights remain research-dependent
and must be referenced, experimentally calibrated, and documented.


---

## 12. Unified Flow Observation

The adaptive framework requires a common observation unit that
combines end-to-end QoS measurements with controller-observed
data-plane telemetry.

Each monitored flow should be represented by a Unified Flow
Observation containing:

### Flow Identity

- flow ID
- source host
- destination host
- timestamp

### End-to-End QoS Metrics

Collected from monitoring or experiment traffic:

- RTT
- delay
- jitter
- packet loss
- throughput

### Actual Flow Path

The observation must identify the network path used by the flow.

Example:

    h1 -> s1 -> s2 -> s4 -> h2

Represented as:

    [1, 2, 4]

The framework must not assume or manually assign the path.
Path information should be derived from controller topology and
forwarding information.

### Path-Specific Data-Plane Telemetry

Only telemetry belonging to links on the actual flow path should
be associated with the flow.

Examples:

- link throughput
- packet rate
- TX/RX errors
- TX/RX byte counters
- TX/RX packet counters
- port statistics

The framework must not attach unrelated network-wide link metrics
to every flow.

### Controller and Network State

The observation may also include:

- active datapaths
- topology switch count
- topology link count
- controller connectivity
- relevant topology changes

The resulting observation conceptually becomes:

    Flow Identity
          +
    End-to-End QoS
          +
    Actual Flow Path
          +
    Path-Specific Data-Plane Telemetry
          +
    Controller / Network State
          =
    Unified Flow Observation

This Unified Flow Observation is the common input for:

- historical QoS analysis
- degradation detection
- GRU time-series prediction
- DRL state construction
- adaptive recovery verification

The framework should initially preserve raw measured values.
QoS thresholds, normalization bounds, composite scores and metric
weights must not be assigned arbitrarily. They must be referenced,
experimentally calibrated, and documented.

---

## 13. Observation Time-Series

Unified Flow Observations should be collected continuously over time.

    Observation t1
            |
            v
    Observation t2
            |
            v
    Observation t3
            |
            v
          ...

Each observation should preserve:

- timestamp
- flow identity
- end-to-end QoS metrics
- actual path
- path-specific telemetry
- relevant controller state

The resulting time-series becomes the evidence base for:

- baseline analysis
- controlled degradation experiments
- degradation detection
- GRU dataset preparation
- recovery evaluation

Before implementing prediction or recovery policies, the framework
must verify that controlled network changes produce measurable and
correctly recorded changes in the observations.


# ============================================================
# PATH RECOVERY ENGINE - CURRENT IMPLEMENTATION AND NEXT STEPS
# ============================================================

## Current Development Update

A modular path recovery service has been developed:

    open_sdn_lab_path_recovery.py

The service is intended to provide the core adaptive routing and
link evaluation logic for OpenSDNLab.

Current capabilities include:

- Normalized bidirectional logical link mapping.
- LinkMetricsMatrix for topology-wide link storage.
- Dynamic link metric evaluation.
- Link health classification.
- QoS-aware link weight calculation.
- Congestion-aware path avoidance.
- Constrained shortest path recovery.
- Multiplicative path packet-loss calculation.
- PATH_RECOVERY state transitions.

---

## Normalized Bidirectional Link Mapping

OpenFlow port statistics are directional.

Example:

    s1:port2  --->  s2:port1
    s2:port1  --->  s1:port2

The LinkMetricsMatrix normalizes directional measurements into one
logical bidirectional link.

Each logical link may contain:

- forward metrics
- reverse metrics
- utilization
- packet rate
- error rate
- packet-loss estimate
- aggregated metrics
- health state
- timestamp

The objective is to prevent directional OpenFlow port statistics from
being treated as separate network links.

---

## Dynamic Link Health

Logical links are evaluated using dynamic network measurements.

Health states:

    NORMAL
    DEGRADED
    CRITICAL

The OS-Ken controller remains responsible for collecting raw
OpenFlow measurements.

The analysis and recovery layers are responsible for interpreting
those measurements.

Architecture:

    OS-Ken Controller
            |
            v
    OpenFlow Port Statistics
            |
            v
    LinkMetricsMatrix
            |
            v
    Link Health Evaluation
            |
            v
    QoS Analysis / Recovery

QoS policy interpretation should remain decoupled from the low-level
OpenFlow statistics collector.

---

## QoS-Aware Link Weight

The recovery engine uses a QoS-aware link cost.

Conceptually:

    W(e) = alpha * Delay + beta * PacketLoss

High congestion receives a large routing penalty.

The current implementation uses:

    Congestion threshold: 90%
    Congested link penalty: 10000.0

These values should remain configurable.

The purpose is to make highly congested or degraded links unattractive
during recovery path selection.

---

## Constrained Shortest Path Recovery

The recovery engine provides:

    find_optimal_recovery_path()

The solver evaluates candidate paths using constraints including:

- minimum available bandwidth
- maximum end-to-end delay
- maximum cumulative packet loss
- link utilization
- link health

The objective is not only shortest hop count.

Recovery path selection considers:

    Topology
        +
    Link QoS
        +
    Bandwidth Constraints
        +
    Delay Constraints
        +
    Packet Loss Constraints
        |
        v
    QoS-Aware Recovery Path

---

## Path-Level Packet Loss

Cumulative path packet loss is calculated using success probability.

    PathSuccess =
        Product of (1 - LinkLoss)

Therefore:

    PathLoss =
        1 - Product of (1 - LinkLoss)

This avoids directly adding packet-loss percentages across links.

---

## PATH_RECOVERY Integration

The recovery solver follows the PATH_RECOVERY state model.

    QoS Monitoring
            |
            v
    QoS Degradation Detected
            |
            v
    PATH_RECOVERY_TRIGGERED
            |
            v
    Alternative Path Search
            |
       +----+----+
       |         |
       v         v
    Valid      No Valid
    Path       Path
       |         |
       v         v
    PATH_SELECTED
             PATH_RECOVERY_NO_ALTERNATIVE_PATH
       |
       v
    Path Reconfiguration
       |
   +---+---+
   |       |
   v       v
Success   Failure
   |       |
   v       v
PATH_RECOVERY_EXECUTED
        PATH_RECOVERY_FAILED

---

# NEXT IMPLEMENTATION PRIORITY

The next task is to integrate the path recovery engine into the
real OpenSDNLab architecture.

Target:

    Real OpenFlow Network
            |
            v
    OS-Ken Topology Discovery
            |
            v
    OS-Ken Port Statistics
            |
            v
    LinkMetricsMatrix
            |
            v
    Live Link Health
            |
            v
    QoS Constraint Solver
            |
            v
    Recovery Path
            |
            v
    OpenFlow Path Enforcement
            |
            v
    Traffic Recovery Evaluation

Required work:

1. Add the path recovery service to the OpenSDNLab architecture.
2. Connect real OS-Ken topology to LinkMetricsMatrix.
3. Feed live OpenFlow port statistics into logical links.
4. Continuously update link metrics and health.
5. Trigger PATH_RECOVERY from actual QoS degradation.
6. Execute find_optimal_recovery_path().
7. Validate the selected recovery path.
8. Implement OpenFlow path enforcement.
9. Measure recovery time, packet loss, delay, jitter and throughput.

---

# FUTURE DEVELOPMENT ORDER

Phase 1:

    Real Link Metrics Integration

Phase 2:

    Live LinkMetricsMatrix

Phase 3:

    Path-Level QoS Aggregation

Phase 4:

    Real PATH_RECOVERY Trigger

Phase 5:

    OpenFlow Recovery Enforcement

Phase 6:

    Fast Failover Baseline

Phase 7:

    Recovery Evaluation and Historical Data Collection

Phase 8:

    GRU Dataset Preparation and Offline Training

Phase 9:

    Asynchronous GRU Prediction Service

Phase 10:

    DRL Adaptive Decision Engine

Phase 11:

    Segment Routing / TI-LFA Feasibility Investigation

---

## Core Design Principle

    OpenFlow collects measurements.

    Topology identifies network relationships.

    LinkMetricsMatrix normalizes directional measurements.

    QoS analysis evaluates current network conditions.

    Path recovery selects a valid alternative route.

    OpenFlow enforcement applies the selected route.

    GRU predicts future degradation.

    DRL determines intelligent adaptive actions.

The immediate priority is to validate the path recovery engine using
real OpenSDNLab topology and OpenFlow measurements before moving to
GRU, DRL or native Segment Routing.

# ============================================================
# END PATH RECOVERY ENGINE UPDATE
# ============================================================

