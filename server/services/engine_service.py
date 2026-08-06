"""
OpenSDNLab Engine Service
"""


class EngineService:

    def capabilities(self):

        return {

            "controllers": [
                "osken"
            ],

            "topologies": [
                "linear",
                "tree",
                "mesh",
                "fat-tree",
                "spine-leaf"
            ],

            "protocols": [
                "ipv4",
                "ipv6"
            ],

            "qos": [
                "bandwidth",
                "delay",
                "loss",
                "queue"
            ],

            "metrics": [
                "rtt",
                "throughput",
                "jitter",
                "packet_loss"
            ]

        }

