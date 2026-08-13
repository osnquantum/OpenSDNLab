"""
Research Analytics Service
"""

import statistics

from engine.repository.sqlite.sqlite_repository import SQLiteRepository


class AnalyticsService:


    def __init__(self):

        self.db = SQLiteRepository()



    def experiment_analysis(self, name):

        cursor = self.db.connection.cursor()


        cursor.execute(
            """
            SELECT

            average_rtt,
            jitter,
            throughput,
            packet_loss,
            estimated_one_way_delay

            FROM experiment_runs

            WHERE experiment_id=?

            ORDER BY run_number

            """,
            (name,)
        )


        rows = cursor.fetchall()


        if not rows:

            return {

                "samples": 0,

                "rtt": {
                    "mean": 0,
                    "median": 0,
                    "min": 0,
                    "max": 0,
                    "std": 0
                },

                "jitter": {
                    "mean": 0,
                    "std": 0
                },

                "throughput": {
                    "mean": 0,
                    "min": 0,
                    "max": 0
                },

                "packet_loss": {
                    "mean": 0
                },

                "one_way_delay": {
                    "mean": 0
                }

            }


        rtt = [x[0] for x in rows]
        jitter = [x[1] for x in rows]
        throughput = [x[2] for x in rows]
        loss = [x[3] for x in rows]
        delay = [x[4] for x in rows]
        mos = [x[5] for x in rows]


        return {


            "samples": len(rows),


            "rtt": {

                "mean": statistics.mean(rtt),

                "median": statistics.median(rtt),

                "min": min(rtt),

                "max": max(rtt),

                "std":
                statistics.stdev(rtt)
                if len(rtt) > 1 else 0

            },


            "jitter": {

                "mean": statistics.mean(jitter),

                "std":
                statistics.stdev(jitter)
                if len(jitter) > 1 else 0

            },


            "throughput": {

                "mean": statistics.mean(throughput),

                "min": min(throughput),

                "max": max(throughput)

            },


            "packet_loss": {

                "mean": statistics.mean(loss)

            },


            "one_way_delay": {

                "mean": statistics.mean(delay)

            },


            "mos": {

                "mean": statistics.mean(mos),

                "min": min(mos),

                "max": max(mos)

            }

        }
