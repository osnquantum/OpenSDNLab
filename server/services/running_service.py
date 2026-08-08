"""
Running Experiment Service
"""

from server.services.job_service import JobService


class RunningService:


    def __init__(self):

        self.jobs = JobService()



    def get_status(
        self,
        job_id
    ):

        return self.jobs.get_job(
            job_id
        )
