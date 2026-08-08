from flask import Blueprint, request, jsonify

from engine.repository.sqlite.sqlite_repository import SQLiteRepository
from server.services.statistical_service import StatisticalService


statistical_compare = Blueprint(
    "statistical_compare",
    __name__
)


db = SQLiteRepository()

service = StatisticalService()



def get_metric(exp):

    cursor=db.connection.cursor()


    cursor.execute(
        """
        SELECT average_rtt

        FROM experiment_runs

        WHERE experiment_id=?

        """,
        (exp,)
    )


    return [
        float(row[0])
        for row in cursor.fetchall()
    ]




@statistical_compare.route(
    "/api/analytics/statistical_compare",
    methods=["POST"]
)
def statistical_compare_api():


    body=request.json


    exp_a=body["experiment_a"]

    exp_b=body["experiment_b"]



    a=get_metric(exp_a)

    b=get_metric(exp_b)



    result=service.analyze(
        a,b
    )



    statement=""


    if result["significant"]:

        statement = (
        "Statistically significant "
        "difference detected"
        )

    else:

        statement = (
        "No statistically significant "
        "difference detected"
        )



    return jsonify({

        "success":True,

        "experiment_a":exp_a,

        "experiment_b":exp_b,

        "analysis":result,

        "conclusion":statement

    })
