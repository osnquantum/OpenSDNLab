from flask import Blueprint, jsonify

from server.services.job_service import job_service


live = Blueprint(
    "live",
    __name__
)


@live.route("/api/live/job/<job_id>")
def live_job(job_id):

    job = job_service.get_job(job_id)

    if not job:
        return jsonify({
            "success": False,
            "message": "Job not found"
        }),404


    return jsonify({
        "success": True,
        "data": job
    })
