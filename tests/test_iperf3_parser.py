import json
import unittest

from engine.monitoring.collectors.iperf3_parser import (
    parse_iperf3_mbps,
)


class TestIperf3Parser(unittest.TestCase):

    def test_parses_mbps(self):
        output = json.dumps({
            "end": {
                "sum_received": {
                    "bits_per_second": 2_010_000
                }
            }
        })
        self.assertEqual(parse_iperf3_mbps(output), 2.01)

    def test_preserves_valid_zero(self):
        output = json.dumps({
            "end": {
                "sum_received": {
                    "bits_per_second": 0
                }
            }
        })
        self.assertEqual(parse_iperf3_mbps(output), 0.0)

    def test_rejects_malformed_json(self):
        self.assertIsNone(parse_iperf3_mbps("{invalid json"))

    def test_rejects_missing_measurement(self):
        self.assertIsNone(
            parse_iperf3_mbps(json.dumps({"end": {}}))
        )

    def test_rejects_non_finite_value(self):
        output = json.dumps({
            "end": {
                "sum_received": {
                    "bits_per_second": float("inf")
                }
            }
        })
        self.assertIsNone(parse_iperf3_mbps(output))


if __name__ == "__main__":
    unittest.main()
