# Dynamic Topology Generator

## Objective

Allow users to dynamically create SDN topologies by selecting:

- Number of hosts
- Number of switches
- Topology type
- Link configuration

## Proposed Workflow

User
|
v
Topology Builder UI
|
v
Topology JSON Generator
|
v
Topology Preview
|
v
Mininet Deployment
|
v
Experiment Execution

## Current Status

Design phase.

## Implementation

Pending.

## Testing

Pending.

## Results

Pending.

## Implementation Progress

The topology generation API was extended from parameter-based configuration to graph-based topology generation.

The generated topology contains:

- Network nodes (hosts and switches)
- Link relationships
- Controller information
- Topology metadata

Example generated topology:

Hosts:
5

Switches:
2

Topology:
Linear

The graph representation will be used for:

1. Web-based topology visualization
2. Mininet topology deployment
3. Experiment reproducibility

## Web Topology Visualization

The topology preview interface was modified to consume the generated topology graph JSON directly from the REST API.

The visualization dynamically displays:

- Host nodes
- Switch nodes
- Link relationships

This enables researchers to verify the experiment topology before deployment.

