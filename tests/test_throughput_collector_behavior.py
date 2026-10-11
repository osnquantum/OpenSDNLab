import json
import unittest
from unittest.mock import patch

from engine.monitoring.collectors.throughput_collector import (
    ThroughputCollector,
)


class FakeHost:
    def __init__(self, name, ip, responses=None):
        self.name = name
        self._ip = ip
        self.responses = responses or {}
        self.commands = []

    def IP(self):
        return self._ip

    def cmd(self, command):
        self.commands.append(command)

        if "echo $!" in command:
            parts = command.split()
            self.server_port = parts[parts.index("-p") + 1]
            return "12345\n"

        if "ps -p 12345 -o args=" in command:
            port = getattr(self, "server_port", None)
            if port is not None:
                return f"/usr/bin/iperf3 -s -1 -p {port}\n"
            return ""

        if "SERVER_ALIVE" in command:
            return "SERVER_ALIVE:0\n"

        if "iperf3 -c " in command:
            return self.responses.get("client", "")

        return ""


class TestThroughputCollectorBehavior(unittest.TestCase):

    def setUp(self):
        self.source = FakeHost("h1", "10.0.0.1")
        self.destination = FakeHost("h2", "10.0.0.2")
        self.collector = ThroughputCollector()

    @patch("engine.monitoring.collectors.throughput_collector.MetricCollector")
    @patch("engine.monitoring.collectors.throughput_collector.time.sleep")
    def test_successful_measurement_and_cleanup(self, sleep, metric_collector):
        self.source.responses["client"] = json.dumps({
            "end": {"sum_received": {"bits_per_second": 2_500_000}}
        })

        result = self.collector.collect(
            self.source, self.destination, experiment_id=None, duration=1
        )

        self.assertEqual(result.throughput, 2.5)
        self.assertTrue(any("iperf3 -s -1" in c for c in self.destination.commands))
        self.assertTrue(any("kill 12345" in c for c in self.destination.commands))

    @patch("engine.monitoring.collectors.throughput_collector.time.sleep")
    def test_failed_measurement_is_unavailable_and_cleans_up(self, sleep):
        self.source.responses["client"] = "iperf3: connection failed"

        result = self.collector.collect(
            self.source, self.destination, experiment_id=None, duration=1
        )

        self.assertIsNone(result.throughput)
        self.assertTrue(any("kill 12345" in c for c in self.destination.commands))

    @patch("engine.monitoring.collectors.throughput_collector.time.sleep")
    def test_server_startup_failure_does_not_run_client(self, sleep):
        original_cmd = self.destination.cmd

        def failing_server_cmd(command):
            if "echo $!" in command:
                parts = command.split()
                self.destination.server_port = parts[parts.index("-p") + 1]
                return "12345\n"
            if "ps -p 12345 -o args=" in command:
                port = getattr(self.destination, "server_port", None)
                if port is not None:
                    return f"/usr/bin/iperf3 -s -1 -p {port}\n"
                return ""
            if "SERVER_ALIVE" in command:
                return "SERVER_ALIVE:1\nAddress already in use\n"
            return original_cmd(command)

        self.destination.cmd = failing_server_cmd

        result = self.collector.collect(
            self.source, self.destination, experiment_id=None, duration=1
        )

        self.assertIsNone(result.throughput)
        self.assertFalse(any("iperf3 -c " in c for c in self.source.commands))
        self.assertTrue(any("kill 12345" in c for c in self.destination.commands))

    @patch("engine.monitoring.collectors.throughput_collector.time.sleep")
    def test_missing_server_pid_returns_unavailable(self, sleep):
        self.destination.cmd = lambda command: ""

        result = self.collector.collect(
            self.source, self.destination, experiment_id=None, duration=1
        )

        self.assertIsNone(result.throughput)


if __name__ == "__main__":
    unittest.main()
