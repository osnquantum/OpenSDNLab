"""
Controller Process Resource Monitor
"""

import psutil

from engine.controllers.monitoring.base_monitor import BaseControllerMonitor


class ProcessMonitor(BaseControllerMonitor):

    def collect(self, controller):

        status = controller.status()

        pid = status.get("pid")

        if not pid:
            return {
                "controller_process": "DOWN"
            }

        try:

            process = psutil.Process(
                int(pid)
            )

            return {

                "cpu_usage":
                    process.cpu_percent(
                        interval=0.5
                    ),

                "memory_mb":
                    round(
                        process.memory_info().rss
                        /
                        (1024 * 1024),
                        2
                    ),

                "threads":
                    process.num_threads(),

                "process_status":
                    process.status()

            }

        except psutil.NoSuchProcess:

            return {

                "controller_process":
                "NOT_FOUND"

            }
