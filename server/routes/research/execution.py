from flask import Blueprint, jsonify

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
        protocol,
        controller

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
    exp.protocol = row[5]
    exp.controller = row[6]


    result = executor.execute(exp)


    return jsonify(result)

