from engine.dashboard.batch_manager import BatchManager
from engine.execution.experiment_executor import ExperimentExecutor
from engine.repository.sqlite.sqlite_repository import SQLiteRepository


class BatchExecutor:


    def __init__(self):

        self.database = SQLiteRepository()

        self.batch_manager = BatchManager(
            self.database
        )

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


        results = []


        for i in range(total_runs):

            try:

                result = self.executor.execute(
                    experiment
                )


                self.batch_manager.update_progress(
                    job_id,
                    True
                )


                results.append({

                    "run": i + 1,

                    "success": True,

                    "result": result

                })


            except Exception as e:


                self.batch_manager.update_progress(
                    job_id,
                    False
                )


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
