"""
CDF Latency Analysis API
"""

from flask import Blueprint, jsonify

from engine.repository.sqlite.sqlite_repository import SQLiteRepository


cdf = Blueprint(
    "cdf",
    __name__
)


db = SQLiteRepository()



@cdf.route(
    "/api/analytics/cdf/<experiment_id>"
)
def cdf_data(experiment_id):


    cursor = db.connection.cursor()


    cursor.execute(
        """
        SELECT

        average_rtt

        FROM experiment_runs

        WHERE experiment_id=?

        ORDER BY average_rtt

        """,
        (experiment_id,)
    )


    rows = cursor.fetchall()


    if not rows:

        return jsonify({

            "success":False,

            "message":"No data found"

        })



    rtt = [

        float(row[0])

        for row in rows

    ]


    total=len(rtt)



    cdf=[]


    for i,value in enumerate(rtt):

        cdf.append({

            "x":value,

            "y":
            round(
                (i+1)/total,
                4
            )

        })



    return jsonify({

        "success":True,

        "experiment":
        experiment_id,

        "samples":
        total,

        "cdf":

        cdf

    })
