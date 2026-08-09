from engine.analysis.statistics.statistics_engine import StatisticsEngine
from engine.repository.sqlite.sqlite_repository import SQLiteRepository


class ExperimentAnalysisService:


    def __init__(self):

        self.db = SQLiteRepository()

        self.stats = StatisticsEngine()



    def get_runs(self, experiment_id):

        cursor = self.db.connection.cursor()

        cursor.execute(
            """
            SELECT
                average_rtt,
                jitter,
                throughput,
                packet_loss

            FROM experiment_runs

            WHERE experiment_id=?

            ORDER BY run_number
            """,
            (experiment_id,)
        )


        rows = cursor.fetchall()

        return rows



    def analyze(self, experiment_id):

        rows = self.get_runs(
            experiment_id
        )


        if not rows:
            return {
                "error":"No experiment data found"
            }



        rtt = [
            r[0]
            for r in rows
        ]

        jitter = [
            r[1]
            for r in rows
        ]

        throughput = [
            r[2]
            for r in rows
        ]

        loss = [
            r[3]
            for r in rows
        ]



        return {

            "experiment_id":
                experiment_id,


            "runs":
                len(rows),


            "rtt":
                self.stats.analyze(rtt),


            "jitter":
                self.stats.analyze(jitter),


            "throughput":
                self.stats.analyze(throughput),


            "packet_loss":
                self.stats.analyze(loss)

        }
