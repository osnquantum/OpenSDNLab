from flask import Blueprint, jsonify

from engine.repository.sqlite.sqlite_repository import SQLiteRepository


qos_qoe = Blueprint(
    "qos_qoe",
    __name__
)


db = SQLiteRepository()



@qos_qoe.route(
    "/api/qos-qoe/decisions/<experiment_id>"
)
def get_decisions(experiment_id):

    rows = db.connection.execute(
        """
        SELECT
            run_number,
            action,
            reason,
            created_at

        FROM qos_qoe_decisions

        WHERE experiment_id=?

        ORDER BY run_number
        """,
        (experiment_id,)
    ).fetchall()


    result = []

    for row in rows:

        result.append({

            "run": row[0],
            "action": row[1],
            "reason": row[2],
            "time": row[3]

        })


    return jsonify(result)
