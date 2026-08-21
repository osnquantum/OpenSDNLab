"""
Experiment Running Page
"""

from flask import Blueprint, render_template

from server.services.running_service import RunningService


running = Blueprint(
    "running",
    __name__
)


service = RunningService()



@running.route("/running/<job_id>")
def experiment_running(job_id):

    job = service.get_status(
        job_id
    )


    return render_template(
        "running.html",
        job=job
    )
