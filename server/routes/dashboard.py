from flask import Blueprint, jsonify, render_template

from engine.execution.experiment_executor import ExperimentExecutor
from engine.repository.sqlite.sqlite_repository import SQLiteRepository
from engine.system.runtime_state import RuntimeState


dashboard = Blueprint(
    "dashboard",
    __name__
)


db = SQLiteRepository()

executor = ExperimentExecutor()


current_status = {
    "state": "IDLE",
    "experiment_id": None
}





@dashboard.route(
    "/dashboard",
    methods=["GET"]
)
def dashboard_page():

    return render_template(
        "dashboard/index.html"
    )

@dashboard.route(
    "/api/dashboard/status",
    methods=["GET"]
)
def status():

    return jsonify(current_status)




@dashboard.route(
    "/api/dashboard/run/<experiment_id>",
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



    current_status["state"]="RUNNING"

    current_status["experiment_id"]=experiment_id



    result = executor.execute(exp)



    current_status["state"]="COMPLETED"



    return jsonify(result)


@dashboard.route(
    "/api/dashboard/live",
    methods=["GET"]
)
def live_status():

    return jsonify(
        RuntimeState.get()
    )

