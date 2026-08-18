"""
Dynamic Controller Monitoring Service
"""

from engine.controllers.monitoring.registry import MonitorRegistry
from engine.controllers.monitoring.collectors.process_monitor import ProcessMonitor
from engine.controllers.monitoring.collectors.openflow_monitor import OpenFlowMonitor


class ControllerMonitor:

    def __init__(self):

        self.registry = MonitorRegistry()

        self.registry.register(
            ProcessMonitor()
        )

        self.registry.register(
            OpenFlowMonitor()
        )


    def collect(self, controller):

        return {

            "controller":
                controller.name(),

            "metrics":
                self.registry.collect(
                    controller
                )

        }
