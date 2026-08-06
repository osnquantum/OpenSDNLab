"""
Experiment Repository

Stores experiment results as JSON.
"""

import json
from dataclasses import asdict
from pathlib import Path

from repository.models import ExperimentResult


class ExperimentRepository:

    def __init__(self):

        self.output_dir = Path("results")

        self.output_dir.mkdir(exist_ok=True)

    ###########################################################

    def save(self, result: ExperimentResult):

        filename = self.output_dir / (
            result.experiment_name.replace(" ", "_").lower()
            + ".json"
        )

        data = asdict(result)

        data["created_at"] = str(result.created_at)

        with open(filename, "w") as f:

            json.dump(

                data,

                f,

                indent=4

            )

        return filename

