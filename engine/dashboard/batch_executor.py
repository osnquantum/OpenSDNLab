from engine.core.logger import logger
from engine.dashboard.batch_manager import BatchManager
from engine.execution.experiment_executor import ExperimentExecutor
from engine.repository.sqlite.sqlite_repository import SQLiteRepository


class BatchExecutor:


    def __init__(self):

        self.database = SQLiteRepository()

        self.batch_manager = BatchManager()

        self.executor = ExperimentExecutor()



    def run_batch(
        self,
        job_id,
        experiment,
        total_runs
    ):


        self.batch_manager.start_batch(
            job_id
        )

        self.database.connection.execute(
            "UPDATE batch_jobs SET status=? WHERE job_id=?",
            ("RUNNING", job_id)
        )
        self.database.connection.commit()

        results = []


        for i in range(total_runs):

            try:

                result = self.executor.execute(
                    experiment,
                    job=job_id
                )


                progress = self.batch_manager.update_progress(
                    job_id,
                    True
                )

                self.database.connection.execute(
                    """UPDATE batch_jobs
                       SET current_run=?,
                           successful=?,
                           failed=?,
                           status=?
                       WHERE job_id=?""",
                    (
                        progress["current_run"],
                        progress["successful"],
                        progress["failed"],
                        progress["status"],
                        job_id
                    )
                )
                self.database.connection.commit()

                results.append({

                    "run": i + 1,

                    "success": True,

                    "result": result

                })


            except Exception as e:

                import traceback

                logger.exception(
                    f"BATCH RUN {i + 1} FAILED: {e}"
                )

                print(
                    f"===== BATCH RUN {i + 1} FAILED =====",
                    flush=True
                )

                traceback.print_exc()

                progress = self.batch_manager.update_progress(
                    job_id,
                    False
                )

                self.database.connection.execute(
                    """UPDATE batch_jobs
                       SET current_run=?,
                           successful=?,
                           failed=?,
                           status=?
                       WHERE job_id=?""",
                    (
                        progress["current_run"],
                        progress["successful"],
                        progress["failed"],
                        progress["status"],
                        job_id
                    )
                )
                self.database.connection.commit()

                results.append({

                    "run": i + 1,

                    "success": False,

                    "error": str(e)

                })


        return {

            "job_id": job_id,

            "results": results,

            "status":
                self.batch_manager.get_status(
                    job_id
                )

        }
