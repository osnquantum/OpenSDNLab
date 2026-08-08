"""
OpenSDNLab Experiment Comparator

Compares two or more SDN experiments.
"""

class ExperimentComparator:


    def compare(
        self,
        exp_a,
        exp_b
    ):

        result = {}


        metrics = [
            "average_rtt",
            "jitter",
            "throughput",
            "packet_loss",
            "one_way_delay"
        ]


        for metric in metrics:

            a = exp_a.get(
                metric,
                0
            )

            b = exp_b.get(
                metric,
                0
            )


            if a != 0:

                change = (
                    (b-a)/a
                ) * 100

            else:

                change = 0


            result[metric] = {

                "experiment_a":
                a,

                "experiment_b":
                b,

                "percentage_change":
                change

            }


        return result
