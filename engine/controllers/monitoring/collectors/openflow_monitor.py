"""
OpenFlow Controller Statistics Monitor
"""

import json
from pathlib import Path

from engine.controllers.monitoring.base_monitor import BaseControllerMonitor


class OpenFlowMonitor(BaseControllerMonitor):

    def collect(self, controller):

        path = Path(
            "runtime/controller_stats/osken.json"
        )

        if not path.exists():

            return {
                "switch_count": 0,
                "packet_in_count": 0,
                "flow_install_count": 0
            }

        try:

            with open(path) as f:
                stats = json.load(f)

            return {

                "switch_count":
                    stats.get(
                        "switch_count",
                        0
                    ),

                "packet_in_count":
                    stats.get(
                        "packet_in_count",
                        0
                    ),

                "flow_install_count":
                    stats.get(
                        "flow_install_count",
                        0
                    )

            }

        except Exception:

            return {

                "switch_count": 0,
                "packet_in_count": 0,
                "flow_install_count": 0

            }
