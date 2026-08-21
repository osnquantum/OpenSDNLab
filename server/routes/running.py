"""
Experiment Running Page
"""

from flask import Blueprint, render_template, jsonify, redirect

from server.services.running_service import RunningService
from engine.repository.sqlite.sqlite_repository import SQLiteRepository


running = Blueprint(
    "running",
    __name__
)


service = RunningService()


def resolve_job_id(identifier):

    """
    Accept either:
    - JOB-xxxxxxxx
    - experiment UUID

    If an experiment UUID is supplied, resolve it
    to the latest batch job for that experiment.
    """

    if identifier.startswith("JOB-"):
        return identifier

    db = SQLiteRepository()

    row = db.connection.execute(
        """
        SELECT job_id
        FROM batch_jobs
        WHERE experiment_id=?
        ORDER BY id DESC
        LIMIT 1
        """,
        (identifier,)
    ).fetchone()

    if row:
        return row[0]

    return identifier


@running.route("/running/<job_id>")
def experiment_running(job_id):

    resolved_job_id = resolve_job_id(job_id)

    # Prevent experiment UUIDs from remaining in the URL.
    if resolved_job_id != job_id:
        return redirect(
            "/running/" + resolved_job_id
        )

    job = service.get_status(
        resolved_job_id
    )

    if not job:

        job = {
            "id": resolved_job_id,
            "job_id": resolved_job_id,
            "status": "UNKNOWN",
            "progress": 0,
            "logs": []
        }

    return render_template(
        "running.html",
        job=job
    )


@running.route(
    "/api/running/<job_id>",
    methods=["GET"]
)
def running_status(job_id):

    resolved_job_id = resolve_job_id(job_id)

    job = service.get_status(
        resolved_job_id
    )

    if not job:

        return jsonify({
            "success": False,
            "message": "Job not found",
            "data": None
        }), 404

    return jsonify({
        "success": True,
        "data": job
    })
