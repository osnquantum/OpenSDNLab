"""
Campaign Analysis Service

Aggregates multiple SDN experiments
for research-level comparison.
"""

import sqlite3
from pathlib import Path
from statistics import mean


DB_PATH = "storage/database/opensdnlab.db"



class CampaignAnalysisService:


    def __init__(self):

        self.connection = sqlite3.connect(
            DB_PATH,
            check_same_thread=False
        )



    def analyze_campaign(self, group_id):


        cursor = self.connection.cursor()


        cursor.execute(
            """
            SELECT

            experiment_id,
            experiment_name,
            controller

            FROM experiments

            WHERE group_id=?

            """,
            (group_id,)
        )


        experiments = cursor.fetchall()



        result = {


            "group_id": group_id,

            "total_experiments":
                len(experiments),

            "experiments":[],

            "controller_summary":{}

        }



        controller_data={}



        for exp in experiments:


            exp_id = exp[0]


            cursor.execute(
                """
                SELECT

                AVG(average_rtt),
                AVG(throughput),
                AVG(jitter),
                AVG(packet_loss)

                FROM experiment_runs

                WHERE experiment_id=?

                """,
                (exp_id,)
            )


            metrics = cursor.fetchone()



            item={

                "experiment_id":exp_id,

                "name":exp[1],

                "controller":exp[2],

                "metrics":{

                    "rtt":metrics[0],

                    "throughput":metrics[1],

                    "jitter":metrics[2],

                    "packet_loss":metrics[3]

                }

            }



            result["experiments"].append(item)



            controller = exp[2]


            if controller not in controller_data:

                controller_data[controller]=[]


            if metrics[0]:

                controller_data[controller].append(
                    metrics[0]
                )



        for controller, values in controller_data.items():

            result["controller_summary"][controller]={

                "average_rtt":
                    mean(values),

                "experiments":
                    len(values)

            }



        return result
