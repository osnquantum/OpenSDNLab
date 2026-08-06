"""
Job Execution Service
"""

from datetime import datetime

from engine.jobs.job_status import JobStatus
from engine.services.experiment_manager import ExperimentManager


class JobExecutionService:

    def __init__(self):

        self.manager = ExperimentManager()

    ############################################################

    def execute(self, job):

        job.status = JobStatus.RUNNING
        job.started_at = datetime.now()
        job.progress = 0

        job.add_log("Starting experiment...")

        try:

            ####################################################
            # Execute experiment
            ####################################################

            result = self.manager.run(
                job.configuration
            )

            job.result = result

            job.progress = 100

            job.status = JobStatus.COMPLETED

            job.finished_at = datetime.now()

            job.add_log("Experiment completed successfully.")

        except Exception as error:

            job.status = JobStatus.FAILED

            job.finished_at = datetime.now()

            job.add_log(str(error))

            raise

        return job

