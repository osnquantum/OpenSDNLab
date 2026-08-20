"""
Dynamic Research Analytics Data API
"""

from flask import Blueprint, jsonify, request

from engine.repository.sqlite.sqlite_repository import SQLiteRepository

analytics_data = Blueprint("analytics_data", __name__)


db = SQLiteRepository()


@analytics_data.route("/api/analytics/data/<experiment_id>")
def analytics_dataset(experiment_id):

    cursor = db.connection.cursor()

    job_id = request.args.get("job_id")

    if job_id:

        cursor.execute(
            """
            SELECT
                run_number,
                minimum_rtt,
                average_rtt,
                maximum_rtt,
                jitter,
                packet_loss,
                throughput,
                estimated_one_way_delay,
                mos

            FROM experiment_runs

            WHERE experiment_id=?
              AND job_id=?

            ORDER BY run_number

            """,
            (experiment_id, job_id),
        )

    else:

        cursor.execute(
            """
            SELECT
                run_number,
                minimum_rtt,
                average_rtt,
                maximum_rtt,
                jitter,
                packet_loss,
                throughput,
                estimated_one_way_delay,
                mos

            FROM experiment_runs

            WHERE experiment_id=?

            ORDER BY run_number

            """,
            (experiment_id,),
        )

    rows = cursor.fetchall()

    if not rows:

        return jsonify({"success": False, "message": "No experiment data found"})

    data = {
        "runs": [],
        "rtt": [],
        "minimum_rtt": [],
        "maximum_rtt": [],
        "jitter": [],
        "packet_loss": [],
        "throughput": [],
        "one_way_delay": [],
        "mos": [],
    }

    for row in rows:

        data["runs"].append(row[0])

        data["minimum_rtt"].append(row[1])

        data["rtt"].append(row[2])

        data["maximum_rtt"].append(row[3])

        data["jitter"].append(row[4])

        data["packet_loss"].append(row[5])

        data["throughput"].append(row[6])

        data["one_way_delay"].append(row[7])

        data["mos"].append(row[8])

    return jsonify(
        {
            "success": True,
            "experiment": experiment_id,
            "samples": len(rows),
            "data": data,
        }
    )


@analytics_data.route("/api/analytics/metrics/<experiment_id>")
def analytics_metrics(experiment_id):

    rows = db.connection.execute(
        """
        SELECT
        run_number,
        average_rtt,
        jitter,
        packet_loss,
        throughput
        FROM experiment_runs
        WHERE experiment_id=?
        ORDER BY run_number
        """,
        (experiment_id,),
    ).fetchall()

    return jsonify(
        [
            {"run": r[0], "rtt": r[1], "jitter": r[2], "loss": r[3], "throughput": r[4]}
            for r in rows
        ]
    )


@analytics_data.route("/api/analytics/advanced/<experiment_id>")
def advanced_metrics(experiment_id):

    rows = db.connection.execute(
        """
        SELECT
        run_number,
        average_rtt,
        jitter,
        packet_loss,
        throughput
        FROM experiment_runs
        WHERE experiment_id=?
        ORDER BY run_number
        """,
        (experiment_id,),
    ).fetchall()

    return jsonify(
        {
            "runs": [r[0] for r in rows],
            "rtt": [r[1] for r in rows],
            "jitter": [r[2] for r in rows],
            "loss": [r[3] for r in rows],
            "throughput": [r[4] for r in rows],
        }
    )
