"""
Scenario-Aware QoS Dataset Builder

Creates GRU-ready QoS sequences without mixing
different network scenarios or crossing experiment boundaries.
"""

import sqlite3


class ScenarioDataset:


    FEATURES = [

        "average_rtt",
        "jitter",
        "packet_loss",
        "throughput",
        "mos"

    ]


    def __init__(self, database_path):

        self.database_path = database_path


    def normalize_text(self, value):

        if value is None:
            return None

        return str(value).strip().lower()


    def normalize_scenario(self, row):

        return {

            "topology":
                self.normalize_text(row["topology"]),

            "hosts":
                row["hosts"],

            "switches":
                row["switches"],

            "traffic_type":
                self.normalize_text(
                    row["traffic_type"]
                ),

            "controller":
                self.normalize_text(
                    row["controller"]
                ),

            "bandwidth":
                row["bandwidth"],

            "delay":
                self.normalize_text(
                    row["delay"]
                )

        }


    def scenario_key(self, scenario):

        return (

            scenario["topology"],

            scenario["hosts"],

            scenario["switches"],

            scenario["traffic_type"],

            scenario["controller"],

            scenario["bandwidth"],

            scenario["delay"]

        )


    def load_experiments(self):

        db = sqlite3.connect(
            self.database_path
        )

        db.row_factory = sqlite3.Row

        rows = db.execute(
            """
            SELECT
                experiment_id,
                topology,
                hosts,
                switches,
                traffic_type,
                controller,
                bandwidth,
                delay

            FROM experiments
            """
        ).fetchall()

        db.close()

        return rows


    def load_runs(self, experiment_id):

        db = sqlite3.connect(
            self.database_path
        )

        db.row_factory = sqlite3.Row

        rows = db.execute(
            """
            SELECT
                run_number,
                average_rtt,
                jitter,
                packet_loss,
                throughput,
                mos,
                created_at

            FROM experiment_runs

            WHERE experiment_id = ?

            ORDER BY run_number ASC
            """,
            (
                experiment_id,
            )
        ).fetchall()

        db.close()

        return rows


    def build_sequences(
        self,
        minimum_runs=5
    ):

        datasets = {}

        experiments = (
            self.load_experiments()
        )


        for experiment in experiments:

            scenario = (
                self.normalize_scenario(
                    experiment
                )
            )

            key = (
                self.scenario_key(
                    scenario
                )
            )

            runs = (
                self.load_runs(
                    experiment[
                        "experiment_id"
                    ]
                )
            )


            if len(runs) < minimum_runs:

                continue


            sequence = []


            for run in runs:

                values = []

                valid = True


                for feature in self.FEATURES:

                    value = run[
                        feature
                    ]


                    if value is None:

                        valid = False

                        break


                    values.append(
                        float(value)
                    )


                if valid:

                    sequence.append(
                        values
                    )


            if len(sequence) < minimum_runs:

                continue


            if key not in datasets:

                datasets[key] = []


            datasets[key].append({

                "experiment_id":
                    experiment[
                        "experiment_id"
                    ],

                "scenario":
                    scenario,

                "sequence":
                    sequence

            })


        return datasets
