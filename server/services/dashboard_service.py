"""
Dashboard Data Service
"""

from engine.repository.sqlite.sqlite_repository import SQLiteRepository


class DashboardService:


    def __init__(self):

        self.database = SQLiteRepository()



    def get_dashboard_data(self):

        cursor = self.database.connection.cursor()


        cursor.execute(
            """
            SELECT

            experiment_name,
            average_rtt,
            jitter,
            packet_loss,
            throughput,
            one_way_delay,
            status

            FROM experiments

            ORDER BY id DESC

            LIMIT 1

            """
        )


        row = cursor.fetchone()


        if not row:

            return {

                "experiment_name":"No experiment",

                "average_rtt":0,

                "jitter":0,

                "packet_loss":0,

                "throughput":0,

                "one_way_delay":0,

                "status":"IDLE"

            }


        return {

            "experiment_name":row[0],

            "average_rtt":row[1],

            "jitter":row[2],

            "packet_loss":row[3],

            "throughput":row[4],

            "one_way_delay":row[5],

            "status":row[6]

        }
