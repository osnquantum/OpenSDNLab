"""
OpenSDNLab CSV Exporter

Exports experiment runs for research analysis.
"""

import csv
from pathlib import Path


class CSVExporter:


    def export_runs(
        self,
        experiment_id,
        runs
    ):

        directory = Path(
            "storage/results"
        ) / experiment_id

        directory.mkdir(
            parents=True,
            exist_ok=True
        )


        file = directory / "raw_measurements.csv"


        with open(
            file,
            "w",
            newline=""
        ) as f:


            writer = csv.writer(f)


            writer.writerow([

                "run_number",
                "average_rtt",
                "jitter",
                "packet_loss",
                "throughput",
                "one_way_delay"

            ])


            for index, run in enumerate(
                runs,
                start=1
            ):

                writer.writerow([

                    index,

                    run["average_rtt"],

                    run["jitter"],

                    run["packet_loss"],

                    run["throughput"],

                    run["one_way_delay"]

                ])


        return str(file)
