"""
Live Job Monitoring API
"""

from flask import Blueprint, jsonify

from server.services.job_service import JobService


live = Blueprint(
    "live",
    __name__
)


service = JobService()



@live.route(
    "/api/live/job/<job_id>"
)
def job_status(job_id):

    job = service.get_job(
        job_id
    )


    return jsonify({

        "success": True,

        "data": job

    })
