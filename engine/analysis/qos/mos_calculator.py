"""
MOS Calculator
Estimated Mean Opinion Score (1-5)
Based on ITU-T E-model approximation
"""

import math


def calculate_mos(rtt, packet_loss):

    if rtt is None:
        return None

    if packet_loss is None:
        packet_loss = 0


    delay = rtt / 2


    Id = 0.024 * delay


    Ie = 30 * math.log(
        1 + packet_loss / 10
    )


    R = 94.2 - Id - Ie


    R = max(
        0,
        min(
            100,
            R
        )
    )


    mos = (
        1
        + 0.035 * R
        + 0.000007 * R * (R - 60) * (100 - R)
    )


    mos = max(
        1.0,
        min(
            4.5,
            mos
        )
    )


    return round(
        mos,
        2
    )
