"""
Dynamic Research Analytics Data API
"""

from flask import Blueprint, jsonify

from engine.repository.sqlite.sqlite_repository import SQLiteRepository


analytics_data = Blueprint(
    "analytics_data",
    __name__
)


db = SQLiteRepository()



@analytics_data.route(
    "/api/analytics/data/<experiment_id>"
)
def analytics_dataset(experiment_id):


    cursor = db.connection.cursor()


    cursor.execute(
        """
        SELECT

        run_number,
        minimum_rtt,
        average_rtt,
        maximum_rtt,
        jitter,
        packet_loss,
        throughput,
        estimated_one_way_delay

        FROM experiment_runs

        WHERE experiment_id=?

        ORDER BY run_number

        """,
        (experiment_id,)
    )


    rows = cursor.fetchall()



    if not rows:

        return jsonify({

            "success":False,

            "message":
            "No experiment data found"

        })



    data = {

        "runs": [],

        "rtt": [],

        "minimum_rtt": [],

        "maximum_rtt": [],

        "jitter": [],

        "packet_loss": [],

        "throughput": [],

        "one_way_delay": []

    }



    for row in rows:


        data["runs"].append(
            row[0]
        )


        data["minimum_rtt"].append(
            row[1]
        )


        data["rtt"].append(
            row[2]
        )


        data["maximum_rtt"].append(
            row[3]
        )


        data["jitter"].append(
            row[4]
        )


        data["packet_loss"].append(
            row[5]
        )


        data["throughput"].append(
            row[6]
        )


        data["one_way_delay"].append(
            row[7]
        )



    return jsonify({

        "success":True,

        "experiment":
        experiment_id,

        "samples":
        len(rows),

        "data":
        data

    })
