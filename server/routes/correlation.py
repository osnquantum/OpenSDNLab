"""
Correlation Analysis API
"""

from flask import Blueprint, jsonify

from engine.repository.sqlite.sqlite_repository import SQLiteRepository
from server.services.correlation_service import CorrelationService


correlation = Blueprint(
    "correlation",
    __name__
)


db = SQLiteRepository()

service = CorrelationService()



@correlation.route(
    "/api/analytics/correlation/<experiment_id>"
)
def correlation_result(experiment_id):


    cursor = db.connection.cursor()


    cursor.execute(
        """
        SELECT

        average_rtt,
        jitter,
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

            "message":"No data found"

        })



    data = {

        "rtt":
        [float(r[0]) for r in rows],


        "jitter":
        [float(r[1]) for r in rows],


        "throughput":
        [float(r[2]) for r in rows],


        "one_way_delay":
        [float(r[3]) for r in rows]

    }



    result = service.analyze(
        data
    )


    return jsonify({

        "success":True,

        "experiment":
        experiment_id,


        "correlation":
        result

    })
