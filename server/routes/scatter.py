"""
Scatter Plot Data API
"""

from flask import Blueprint, jsonify

from engine.repository.sqlite.sqlite_repository import SQLiteRepository


scatter = Blueprint(
    "scatter",
    __name__
)


db = SQLiteRepository()



@scatter.route(
    "/api/analytics/scatter/<experiment_id>"
)
def scatter_data(experiment_id):


    cursor = db.connection.cursor()


    cursor.execute(
        """
        SELECT

        average_rtt,
        throughput,
        jitter,
        estimated_one_way_delay

        FROM experiment_runs

        WHERE experiment_id=?

        ORDER BY run_number

        """,
        (experiment_id,)
    )


    rows = cursor.fetchall()



    data = {


        "rtt_throughput":{

            "x":
            [float(r[0]) for r in rows],

            "y":
            [float(r[1]) for r in rows]

        },


        "rtt_jitter":{

            "x":
            [float(r[0]) for r in rows],

            "y":
            [float(r[2]) for r in rows]

        },


        "delay_throughput":{

            "x":
            [float(r[3]) for r in rows],

            "y":
            [float(r[1]) for r in rows]

        }


    }


    return jsonify({

        "success":True,

        "experiment":experiment_id,

        "data":data

    })
