from flask import Blueprint, jsonify
from engine.core.logger import logger

from engine.execution.experiment_executor import ExperimentExecutor
from engine.repository.sqlite.sqlite_repository import SQLiteRepository


experiment_execution = Blueprint(
    "experiment_execution",
    __name__
)


executor = ExperimentExecutor()

db = SQLiteRepository()


@experiment_execution.route(
    "/api/research/experiment/<experiment_id>/run",
    methods=["POST"]
)
def run_experiment(experiment_id):


    cursor = db.connection.cursor()


    cursor.execute(
        """
        SELECT
        experiment_id,
        experiment_name,
        topology,
        hosts,
        switches,
        links,
        protocol,
        controller,
        bandwidth,
        delay,
        loss,
        prediction_enabled,
        recovery_enabled

        FROM experiments

        WHERE experiment_id=?

        """,
        (experiment_id,)
    )


    row = cursor.fetchone()


    if not row:

        return jsonify({

            "success":False,

            "message":"Experiment not found"

        }),404



    class Experiment:

        pass


    exp = Experiment()

    exp.experiment_id = row[0]
    exp.experiment_name = row[1]
    exp.topology = row[2]
    exp.hosts = row[3]
    exp.switches = row[4]
    exp.links = row[5]
    exp.protocol = row[6]
    exp.controller = row[7]
    exp.bandwidth = row[8]
    exp.delay = row[9]
    exp.loss = row[10]

    # Adaptive control configuration
    exp.prediction_enabled = bool(row[11])
    exp.recovery_enabled = bool(row[12])


    try:

        result = executor.execute(exp)

        return jsonify(result)

    except Exception as e:

        logger.error(
            f"Experiment execution failed for {experiment_id}: {e}"
        )

        return jsonify({

            "success": False,

            "message": str(e),

            "error_type": type(e).__name__,

        }), 500

