from flask import Blueprint, jsonify
from engine.repository.sqlite.sqlite_repository import SQLiteRepository


history = Blueprint(
    "history",
    __name__
)


db = SQLiteRepository()


@history.route("/api/history")
def get_history():

    rows = db.connection.execute(
        """
        SELECT
            experiment_id,
            run_number,
            average_rtt,
            jitter,
            packet_loss,
            throughput
        FROM experiment_runs
        ORDER BY id DESC
        LIMIT 20
        """
    ).fetchall()


    result=[]

    for r in rows:

        result.append({

            "experiment_id": r[0],
            "run_number": r[1],
            "rtt": r[2],
            "jitter": r[3],
            "loss": r[4],
            "throughput": r[5]

        })


    return jsonify(result)
