"""
Delay Laboratory
"""

from labs.lab import Lab

from scenarios.delay.increasing_delay import create


def load():

    return Lab(

        title="Laboratory 1 - Delay Analysis",

        objective="Study the effect of link delay on QoS.",

        theory=(
            "Propagation delay increases "
            "end-to-end latency."
        ),

        scenario=create(),

        questions=[

            "Why did RTT increase?",

            "Why was packet loss unchanged?",

            "How would bandwidth affect RTT?"

        ]

    )
