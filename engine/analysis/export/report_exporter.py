"""
OpenSDNLab Research Report Exporter
"""

import json
from pathlib import Path
from datetime import datetime


class ReportExporter:


    def export(
        self,
        experiment_id,
        configuration,
        statistics
    ):


        directory = Path(
            "storage/results"
        ) / experiment_id


        directory.mkdir(
            parents=True,
            exist_ok=True
        )


        file = directory / "research_report.json"


        report = {

            "experiment_id":
            experiment_id,


            "generated_at":
            str(datetime.now()),


            "configuration":
            configuration,


            "statistics":
            statistics

        }


        with open(
            file,
            "w"
        ) as f:

            json.dump(
                report,
                f,
                indent=4
            )


        return str(file)
