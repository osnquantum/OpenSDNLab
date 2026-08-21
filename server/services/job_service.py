"""
Job Service
"""

from engine.jobs.job_executor import job_executor
from engine.repository.sqlite.sqlite_repository import SQLiteRepository


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
        job = job_executor.job_manager.get(job_id)
        if job is not None:
            return self.serialize_job(job)

        # Batch jobs are persisted outside the in-memory JobManager.
        row = SQLiteRepository().connection.execute(
            """
            SELECT job_id, experiment_id, total_runs, current_run,
                   successful, failed, status, created_at, started_at
            FROM batch_jobs
            WHERE job_id=?
            """,
            (job_id,),
        ).fetchone()
        if row is None:
            return None

        total_runs = row[2] or 0
        current_run = row[3] or 0
        progress = int((current_run / total_runs) * 100) if total_runs else 0

        return {
            "id": row[0],
            "job_id": row[0],
            "name": "Batch Experiment",
            "experiment_id": row[1],
            "status": row[6] or "CREATED",
            "progress": progress,
            "total_runs": total_runs,
            "current_run": current_run,
            "successful": row[4] or 0,
            "failed": row[5] or 0,
            "configuration": None,
            "result": None,
            "logs": [],
            "created_at": str(row[7]) if row[7] is not None else None,
            "started_at": str(row[8]) if row[8] is not None else None,
            "finished_at": None,
        }


    def latest_job(self):

        jobs = job_executor.job_manager.list()

        if not jobs:
            return None

        return self.serialize_job(
            jobs[-1]
        )



job_service = JobService()
