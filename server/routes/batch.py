from flask import Blueprint, jsonify, request

from engine.dashboard.experiment_manager import ExperimentManager
from engine.dashboard.batch_executor import BatchExecutor
from engine.dashboard.batch_worker import BatchWorker
from engine.repository.sqlite.sqlite_repository import SQLiteRepository
from engine.dashboard.batch_repository import BatchRepository


batch_api = Blueprint(
    "batch_api",
    __name__
)


experiment_manager = ExperimentManager()

batch_repository = BatchRepository(SQLiteRepository())

batch_executor = None

worker = None

batch_jobs_cache = {}

def get_worker():

    global batch_executor
    global worker


    if worker is None:

        batch_executor = BatchExecutor()

        worker = BatchWorker(
            batch_executor
        )


    return worker





@batch_api.route(
    "/api/batch/create",
    methods=["POST"]
)
def create_batch():


    data = request.json


    experiment_id = data.get(
        "experiment_id"
    )


    runs = data.get(
        "runs",
        1
    )


    job = experiment_manager.create_job(
        experiment_id,
        runs
    )

    batch_jobs_cache[job["job_id"]] = {

        "experiment_id": experiment_id,

        "runs": runs

    }


    return jsonify({

        "success": True,

        "job": job

    })



@batch_api.route(
    "/api/batch/status/<job_id>",
    methods=["GET"]
)
def batch_status(job_id):


    return jsonify({

        "success": True,

        "job":
            batch_repository.get(
                job_id
            )

    })


@batch_api.route(
    "/api/batch/start/<job_id>",
    methods=["POST"]
)
def start_batch(job_id):


    worker = get_worker()


    job = batch_jobs_cache.get(
        job_id
    )


    if not job:

        return jsonify({

            "success":False,

            "message":"Job not found"

        }),404



    worker.start(

        job_id,

        job["experiment_id"],

        job["runs"]

    )


    return jsonify({

        "success": True,

        "message":
            "Batch execution started",

        "job_id":
            job_id

    })


@batch_api.route(
    "/api/batch/latest",
    methods=["GET"]
)
def latest_batch():

    db = SQLiteRepository()

    cursor = db.connection.cursor()

    cursor.execute(
        """
        SELECT
        job_id,
        experiment_id,
        total_runs,
        current_run,
        successful,
        failed,
        status

        FROM batch_jobs

        ORDER BY id DESC

        LIMIT 1
        """
    )

    row = cursor.fetchone()


    if not row:

        return jsonify({
            "success": False,
            "job": None
        })


    return jsonify({

        "success": True,

        "job": {

            "job_id": row[0],

            "experiment_id": row[1],

            "total_runs": row[2],

            "current_run": row[3],

            "successful": row[4],

            "failed": row[5],

            "status": row[6]

        }

    })
