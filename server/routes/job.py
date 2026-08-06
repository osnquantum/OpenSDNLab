"""
Job API
"""

from flask import Blueprint

from server.services.job_service import job_service
from server.utils.api_response import success


job = Blueprint(
    "job",
    __name__
)


@job.route(
    "/jobs",
    methods=["GET"]
)
def list_jobs():

    jobs = job_service.list_jobs()

    return success(
        jobs,
        "Jobs loaded successfully."
    )



@job.route(
    "/jobs/<job_id>",
    methods=["GET"]
)
def get_job(job_id):

    result = job_service.get_job(
        job_id
    )

    if result is None:

        return success(
            {},
            "Job not found."
        )


    return success(
        result,
        "Job loaded successfully."
    )
