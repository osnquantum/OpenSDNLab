"""
Controller Monitor Registry
"""


class MonitorRegistry:

    def __init__(self):

        self.monitors = []


    def register(self, monitor):

        self.monitors.append(
            monitor
        )


    def collect(self, controller):

        result = {}

        for monitor in self.monitors:

            result.update(
                monitor.collect(controller)
            )

        return result
