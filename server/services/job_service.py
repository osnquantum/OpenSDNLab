"""
Job Service
"""

from engine.jobs.job_executor import job_executor


class JobService:


    def serialize_job(self, job):

        if job is None:
            return None


        return {

            "id": job.id,

            "name": job.name,

            "status": job.status.name,

            "progress": job.progress,

            "configuration": str(
                job.configuration
            ),

            "result": job.result,

            "logs": job.logs,

            "created_at": str(
                job.created_at
            ),

            "started_at": str(
                job.started_at
            ) if job.started_at else None,

            "finished_at": str(
                job.finished_at
            ) if job.finished_at else None
        }



    def list_jobs(self):

        jobs = job_executor.job_manager.list()

        return [
            self.serialize_job(job)
            for job in jobs
        ]



    def get_job(self, job_id):

        job = job_executor.job_manager.get(
            job_id
        )

        return self.serialize_job(
            job
        )


    def latest_job(self):

        jobs = job_executor.job_manager.list()

        if not jobs:
            return None

        return self.serialize_job(
            jobs[-1]
        )



job_service = JobService()
