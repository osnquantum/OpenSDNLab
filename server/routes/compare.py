"""
Experiment Comparison API
"""

from flask import Blueprint, request, jsonify

from engine.repository.sqlite.sqlite_repository import SQLiteRepository
from server.services.comparison_service import ComparisonService



compare = Blueprint(
    "compare",
    __name__
)


db = SQLiteRepository()

service = ComparisonService()



def get_experiment_data(exp):


    cursor = db.connection.cursor()


    cursor.execute(
        """
        SELECT

        average_rtt,
        throughput,
        jitter,
        packet_loss

        FROM experiment_runs

        WHERE experiment_id=?

        ORDER BY run_number

        """,
        (exp,)
    )


    rows = cursor.fetchall()



    return {


        "rtt":

        [
            float(r[0])
            for r in rows
        ],


        "throughput":

        [
            float(r[1])
            for r in rows
        ],


        "jitter":

        [
            float(r[2])
            for r in rows
        ],


        "packet_loss":

        [
            float(r[3])
            for r in rows
        ]

    }





@compare.route(
    "/api/analytics/compare",
    methods=["POST"]
)
def compare_experiments():


    body=request.json


    exp_a=body["experiment_a"]

    exp_b=body["experiment_b"]



    data_a=get_experiment_data(exp_a)

    data_b=get_experiment_data(exp_b)



    result=service.summarize(
        data_a,
        data_b
    )



    return jsonify({

        "success":True,

        "experiment_a":exp_a,

        "experiment_b":exp_b,

        "comparison":result

    })
