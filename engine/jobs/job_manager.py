"""
Experiment Job Manager
"""

from engine.jobs.job_status import JobStatus


class JobManager:

    def __init__(self):

        self.jobs = {}

    ############################################################

    def submit(self, job):

        job.status = JobStatus.QUEUED

        job.add_log("Job submitted.")

        self.jobs[job.id] = job

        return job.id

    ############################################################

    def start(self, job):

        job.status = JobStatus.RUNNING

        job.progress = 0

        job.add_log("Experiment started.")

    ############################################################

    def update_progress(self, job, progress):

        job.progress = progress

    ############################################################

    def complete(self, job, result):

        job.status = JobStatus.COMPLETED

        job.progress = 100

        job.result = result

        job.add_log("Experiment completed.")

    ############################################################

    def fail(self, job, message):

        job.status = JobStatus.FAILED

        job.add_log(message)

    ############################################################

    def stop(self, job):

        job.status = JobStatus.STOPPED

        job.add_log("Experiment stopped.")

    ############################################################

    def pause(self, job):

        job.status = JobStatus.PAUSED

        job.add_log("Experiment paused.")

    ############################################################

    def resume(self, job):

        job.status = JobStatus.RUNNING

        job.add_log("Experiment resumed.")

    ############################################################

    def get(self, job_id):

        return self.jobs.get(job_id)

    ############################################################

    def list(self):

        return list(self.jobs.values())

