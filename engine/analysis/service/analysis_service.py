"""
OpenSDNLab Analysis Service

Provides research analysis access
over stored experiments.
"""

from engine.repository.sqlite.sqlite_repository import SQLiteRepository
from engine.analysis.comparison.experiment_comparator import ExperimentComparator


class AnalysisService:


    def __init__(self):

        self.database = SQLiteRepository()

        self.comparator = ExperimentComparator()



    ############################################################
    # Load experiment summary
    ############################################################

    def get_experiment(
        self,
        experiment_id
    ):

        cursor = self.database.connection.cursor()


        cursor.execute(
            """
            SELECT

                experiment_name,
                protocol,
                controller,
                bandwidth,
                delay,
                loss,
                average_rtt,
                jitter,
                throughput,
                packet_loss,
                one_way_delay

            FROM experiments

            WHERE experiment_id = ?

            """,
            (
                experiment_id,
            )
        )


        row = cursor.fetchone()


        if not row:

            return {}


        return {

            "experiment_name": row[0],

            "protocol": row[1],

            "controller": row[2],

            "bandwidth": row[3],

            "delay": row[4],

            "loss": row[5],

            "average_rtt": row[6],

            "jitter": row[7],

            "throughput": row[8],

            "packet_loss": row[9],

            "one_way_delay": row[10]

        }



    ############################################################
    # Compare experiments
    ############################################################

    def compare(
        self,
        experiment_a,
        experiment_b
    ):


        first = self.get_experiment(
            experiment_a
        )


        second = self.get_experiment(
            experiment_b
        )


        return self.comparator.compare(
            first,
            second
        )
