"""
QoE Quality Classification
Based on MOS score
"""


def classify_mos(mos):

    if mos is None:
        return {
            "level": "UNKNOWN",
            "color": "gray"
        }

    if mos >= 4.0:
        return {
            "level": "EXCELLENT",
            "color": "green"
        }

    elif mos >= 3.5:
        return {
            "level": "GOOD",
            "color": "blue"
        }

    elif mos >= 2.5:
        return {
            "level": "FAIR",
            "color": "orange"
        }

    else:
        return {
            "level": "POOR",
            "color": "red"
        }
