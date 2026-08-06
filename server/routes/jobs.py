from flask import Blueprint

from server.services.job_service import job_service
from server.utils.api_response import success

jobs = Blueprint("jobs", __name__)


@jobs.route("/jobs", methods=["GET"])
def get_jobs():

    data = []

    for job in job_service.list_jobs():

        data.append({

            "id": job.id,
            "status": job.status.value,
            "progress": job.progress

        })

    return success(data, "Jobs loaded successfully.")
