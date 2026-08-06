"""
CSV Exporter
"""

import csv
from pathlib import Path


class CSVExporter:

    def export(
        self,
        results,
        filename="results/delay_analysis.csv",
    ):

        output = Path(filename)

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            output,
            "w",
            newline=""
        ) as file:

            writer = csv.writer(file)

            writer.writerow(

                [

                    "Experiment",

                    "Protocol",

                    "Controller",

                    "Bandwidth",

                    "Delay",

                    "Loss",

                    "Minimum RTT",

                    "Average RTT",

                    "Maximum RTT",

                    "Jitter",

                    "Packet Loss",

                    "Throughput"

                ]

            )

            for item in results:

                result = item["result"]

                writer.writerow(

                    [

                        result.experiment_name,

                        result.protocol,

                        result.controller,

                        result.bandwidth,

                        result.delay,

                        result.loss,

                        result.minimum_rtt,

                        result.average_rtt,

                        result.maximum_rtt,

                        result.jitter,

                        result.packet_loss,

                        result.throughput,

                    ]

                )

        return output
