from flask import Blueprint, jsonify, request
from engine.repository.sqlite.sqlite_repository import SQLiteRepository


research_compare = Blueprint(
    "research_compare",
    __name__
)

db = SQLiteRepository()



@research_compare.route("/api/compare/experiments")
def experiments():

    rows=db.connection.execute(
        """
        SELECT DISTINCT experiment_id
        FROM experiment_runs
        ORDER BY experiment_id
        """
    ).fetchall()

    return jsonify(
        [x[0] for x in rows]
    )



@research_compare.route("/api/compare/runs")
def runs():

    exp=request.args.get(
        "experiment_id"
    )

    rows=db.connection.execute(
        """
        SELECT run_number
        FROM experiment_runs
        WHERE experiment_id=?
        ORDER BY run_number
        """,
        (exp,)
    ).fetchall()

    return jsonify(
        [x[0] for x in rows]
    )



@research_compare.route("/api/compare/raw")
def raw():

    exp=request.args.get(
        "experiment_id"
    )

    runs=request.args.get(
        "runs"
    ).split(",")


    result=[]


    for r in runs:

        row=db.connection.execute(
            """
            SELECT
            run_number,
            average_rtt,
            jitter,
            packet_loss,
            throughput

            FROM experiment_runs

            WHERE experiment_id=?
            AND run_number=?

            """,
            (exp,r)
        ).fetchone()


        if row:

            result.append({

            "run":row[0],
            "rtt":row[1],
            "jitter":row[2],
            "loss":row[3],
            "throughput":row[4]

            })


    return jsonify(result)
