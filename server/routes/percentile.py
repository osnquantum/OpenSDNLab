"""
Latency Percentile Analysis API
"""

from flask import Blueprint, jsonify
from engine.repository.sqlite.sqlite_repository import SQLiteRepository


percentile = Blueprint(
    "percentile",
    __name__
)


db = SQLiteRepository()



def calculate_percentile(values, p):

    values = sorted(values)

    if not values:
        return 0


    index = (len(values)-1) * p


    lower = int(index)

    upper = min(
        lower + 1,
        len(values)-1
    )


    weight = index - lower


    return round(
        values[lower] +
        weight *
        (values[upper]-values[lower]),
        3
    )




@percentile.route(
    "/api/analytics/percentile/<experiment_id>"
)
def percentile_data(experiment_id):


    cursor=db.connection.cursor()


    cursor.execute(
        """
        SELECT average_rtt

        FROM experiment_runs

        WHERE experiment_id=?

        ORDER BY average_rtt

        """,
        (experiment_id,)
    )


    rows=cursor.fetchall()


    rtt=[

        float(r[0])

        for r in rows

    ]



    return jsonify({

        "success":True,

        "experiment":
        experiment_id,


        "percentile":{


            "P50":
            calculate_percentile(rtt,0.50),


            "P90":
            calculate_percentile(rtt,0.90),


            "P95":
            calculate_percentile(rtt,0.95),


            "P99":
            calculate_percentile(rtt,0.99)

        },


        "samples":rtt

    })
