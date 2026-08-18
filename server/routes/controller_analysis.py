"""
Controller Impact Analysis API
"""

from flask import Blueprint, jsonify

from engine.repository.sqlite.sqlite_repository import SQLiteRepository
from server.services.controller_analysis_service import ControllerAnalysisService


controller_analysis = Blueprint(
    "controller_analysis",
    __name__
)


db = SQLiteRepository()

service = ControllerAnalysisService()


@controller_analysis.route(
    "/api/analytics/controller-impact/<experiment_id>"
)
def controller_impact(experiment_id):

    cursor = db.connection.cursor()


    cursor.execute(
        """
        SELECT
            er.run_number,
            er.average_rtt,
            cm.metric_name,
            cm.metric_value

        FROM experiment_runs er

        LEFT JOIN controller_metrics cm

        ON er.experiment_id = cm.experiment_id

        AND er.run_number = cm.run_number

        WHERE er.experiment_id=?

        ORDER BY er.run_number

        """,
        (experiment_id,)
    )


    rows = cursor.fetchall()


    if not rows:

        return jsonify({

            "success": False,

            "message":
            "No experiment data found"

        })


    result = {

        "packet_in": [],
        "flows": [],
        "memory": [],
        "rtt": [],
        "runs": []

    }


    run_data = {}


    for run, rtt, name, value in rows:

        if run not in run_data:

            run_data[run] = {

                "run": run,
                "rtt": float(rtt),
                "packet_in": None,
                "flows": None,
                "memory": None

            }


        if name == "packet_in_count":

            run_data[run]["packet_in"] = float(value)


        elif name == "flow_install_count":

            run_data[run]["flows"] = float(value)


        elif name == "memory_mb":

            run_data[run]["memory"] = float(value)



    for run in sorted(run_data):

        item = run_data[run]

        result["runs"].append(item)

        result["rtt"].append(item["rtt"])

        result["packet_in"].append(item["packet_in"])

        result["flows"].append(item["flows"])

        result["memory"].append(item["memory"])


    return jsonify({

        "success": True,

        "experiment":
            experiment_id,

        "samples": {

            "rtt":
                len(result["rtt"]),

            "packet_in":
                len(result["packet_in"]),

            "flows":
                len(result["flows"]),

            "memory":
                len(result["memory"])

        },

        "analysis":
            service.analyze(
                result,
                result
            )

    })
