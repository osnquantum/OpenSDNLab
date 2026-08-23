"""
OpenSDNLab Adaptive State

Creates a normalized observation state for:
- Reactive QoS
- GRU prediction
- DRL decision engine
"""


class AdaptiveState:

    @staticmethod
    def from_metrics(metrics, context=None):

        context = context or {}

        return {
            "average_rtt": float(metrics.get("average_rtt", 0.0)),
            "jitter": float(metrics.get("jitter", 0.0)),
            "packet_loss": float(metrics.get("packet_loss", 0.0)),
            "throughput": float(metrics.get("throughput", 0.0)),
            "mos": float(metrics.get("mos", 0.0)),

            "bandwidth": float(context.get("bandwidth", 0.0)),
            "active_flows": int(context.get("active_flows", 0)),
            "hosts": int(context.get("hosts", 0)),
            "switches": int(context.get("switches", 0)),

            "controller": str(
                context.get("controller", "unknown")
            ),

            # Control-plane state
            "controller_switch_count": int(
                context.get("controller_switch_count", 0)
            ),

            "topology_switch_count": int(
                context.get("topology_switch_count", 0)
            ),

            "topology_link_count": int(
                context.get("topology_link_count", 0)
            ),

            "packet_in_count": int(
                context.get("packet_in_count", 0)
            ),

            "flow_install_count": int(
                context.get("flow_install_count", 0)
            ),

            "run_number": int(
                context.get("run_number", 0)
            ),
        }
