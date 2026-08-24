# OpenSDNLab

Interactive IPv4, IPv6 and SDN Laboratory Platform

Status:

🚧 Under Development

Current Version:

0.1.0-alpha

Author:

Author Dipak KC

Features

- Dynamic Topology Builder
- IPv4 / IPv6 / Dual Stack
- SDN Controller Integration
- QoS Monitoring
- Live Dashboard
- SQLite Database
- Experiment Replay
- Plugin System

License

MIT

---

# Recovery Model

OpenSDNLab distinguishes between monitoring the network and
recovering affected network services.

The primary recovery target is an affected network traffic flow.

Recovery does not mean restoring a QoS score directly. Instead, the
framework observes the condition of network flows and their paths, then
takes an adaptive action when degradation, failure, or another
research-defined recovery condition is detected.

## Recovery Targets

The framework supports three recovery categories.

### 1. Network Connectivity Recovery

Recover network reachability when a network component or path fails.

Examples:

- link failure
- switch failure
- path disconnection

Possible recovery action:

- discover an alternative reachable path
- update forwarding rules
- restore connectivity where an alternative path exists

### 2. QoS and Service Recovery

Recover the performance of an affected traffic flow when its current
network path becomes degraded.

The affected flow may experience degradation in metrics such as:

- delay
- jitter
- packet loss
- throughput
- RTT

Possible recovery actions include:

- keep the current route when recovery is unnecessary
- select an alternative path
- reroute the affected traffic flow
- avoid a failed or degraded network component

The exact degradation and recovery criteria must not be based on
arbitrary thresholds. They must be defined through appropriate
references, application requirements, experimental calibration, or a
documented research methodology.

### 3. Monitoring Coverage Recovery

Monitoring infrastructure must not become a single point of failure.

If a monitoring host or monitoring flow becomes unavailable, the
framework should:

1. remove invalid monitoring flows
2. identify reachable links that are no longer covered
3. generate replacement monitoring candidates
4. select replacement flows
5. restore monitoring coverage

Infrastructure telemetry should continue whenever controller
connectivity remains available.

## Recovery Decision Pipeline

    Actual Traffic Flow
            |
            v
       QoS Monitoring
            |
            v
    Degradation / Failure
       Detection
            |
            +----------------------+
            |                      |
            v                      v
       No Recovery           Recovery Required
            |                      |
            v                      v
    Keep Current Path     Recovery Decision
                                   |
                    +--------------+--------------+
                    |              |              |
                    v              v              v
               Keep Route    Select New Path   Avoid Failed /
                                              Degraded Component
                                   |
                                   v
                       Install Forwarding Rules
                                   |
                                   v
                         Post-Recovery Measurement
                                   |
                                   v
                         Recovery Verification

## DRL Recovery Objective

The DRL component is intended to make recovery decisions for affected
network traffic flows.

The DRL state may include:

- discovered topology
- current path
- alternative reachable paths
- link state
- infrastructure telemetry
- end-to-end QoS observations
- degradation status
- predicted future degradation
- network and controller constraints

Possible actions include:

- keep the current route
- select an alternative path
- reroute an affected flow
- avoid a degraded link
- avoid a failed component
- trigger an appropriate recovery workflow

The final reward function, recovery triggers, QoS normalization bounds,
and metric weights remain research-dependent and must be referenced,
experimentally calibrated, and documented.

## Core Principle

Monitoring flows measure the network.

Traffic flows are the primary objects that may require recovery.

The framework therefore follows the model:

    Observe Network State
            |
            v
    Identify Affected Flow
            |
            v
    Detect or Predict Degradation
            |
            v
    Select Recovery Action
            |
            v
    Apply SDN Forwarding Change
            |
            v
    Measure Post-Recovery State
            |
            v
    Verify Recovery and Learn

