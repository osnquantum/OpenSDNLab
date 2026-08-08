"""
Correlation Matrix API
"""

from flask import Blueprint, jsonify

from engine.repository.sqlite.sqlite_repository import SQLiteRepository
from server.services.matrix_service import MatrixService


matrix = Blueprint(
    "matrix",
    __name__
)


db = SQLiteRepository()

service = MatrixService()



@matrix.route(
    "/api/analytics/matrix/<experiment_id>"
)
def correlation_matrix(experiment_id):


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

            "message":"No experiment data found"

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



    result = service.calculate(data)



    return jsonify({

        "success":True,

        "experiment":experiment_id,

        "matrix":result

    })
