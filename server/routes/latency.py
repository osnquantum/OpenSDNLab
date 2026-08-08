from flask import Blueprint, jsonify

from engine.repository.sqlite.sqlite_repository import SQLiteRepository
from server.services.latency_service import LatencyService


latency = Blueprint(
    "latency",
    __name__
)


db=SQLiteRepository()

service=LatencyService()



@latency.route(
    "/api/analytics/latency/<experiment_id>"
)
def latency_analysis(experiment_id):


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


    values=[

        float(r[0])

        for r in rows

    ]


    result=service.analyze(values)



    return jsonify({

        "success":True,

        "experiment":
        experiment_id,

        **result

    })
