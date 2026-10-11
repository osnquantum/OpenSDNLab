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
        packet_loss = 0.0

    delay = float(rtt) / 2.0

    Id = 0.024 * delay

    Ie = 30.0 * math.log(
        1.0 + float(packet_loss) / 10.0
    )

    R = 94.2 - Id - Ie

    R = max(
        0.0,
        min(100.0, R)
    )

    mos = (
        1.0
        + 0.035 * R
        + 0.000007 * R * (R - 60.0) * (100.0 - R)
    )

    mos = max(
        1.0,
        min(4.5, mos)
    )

    return round(mos, 2)
