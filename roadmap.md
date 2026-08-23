
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
