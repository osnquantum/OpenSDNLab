"""
Running Experiment Service
"""

from server.services.job_service import JobService
from engine.repository.sqlite.sqlite_repository import SQLiteRepository


class RunningService:

    def __init__(self):

        self.jobs = JobService()
        self.database = SQLiteRepository()


    def get_status(self, job_id):

        # --------------------------------------------------------
        # Batch job
        # --------------------------------------------------------

        cursor = self.database.connection.cursor()

        cursor.execute(
            """
            SELECT
                job_id,
                experiment_id,
                total_runs,
                current_run,
                successful,
                failed,
                status
            FROM batch_jobs
            WHERE job_id=?
            """,
            (job_id,)
        )

        row = cursor.fetchone()

        if row:

            total_runs = row[2] or 0
            current_run = row[3] or 0

            progress = (
                int((current_run / total_runs) * 100)
                if total_runs
                else 0
            )

            return {
                "id": row[0],
                "job_id": row[0],
                "experiment_id": row[1],
                "total_runs": total_runs,
                "current_run": current_run,
                "successful": row[4] or 0,
                "failed": row[5] or 0,
                "status": row[6] or "CREATED",
                "progress": progress,
                "logs": []
            }


        # --------------------------------------------------------
        # Normal experiment job
        # --------------------------------------------------------

        return self.jobs.get_job(job_id)
