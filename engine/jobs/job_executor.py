"""
Job Executor
Runs experiments in background.
"""

from datetime import datetime
from threading import Thread, Lock

from engine.jobs.job_manager import JobManager
from engine.jobs.job_status import JobStatus


class JobExecutor:


    def __init__(self):

        self.job_manager = JobManager()

        # Only one Mininet experiment at a time
        self.experiment_lock = Lock()



    def execute(
        self,
        job,
        experiment_manager
    ):

        job.status = JobStatus.QUEUED

        job.add_log(
            "Job queued."
        )


        def worker():

            try:

                with self.experiment_lock:


                    job.started_at = datetime.now()

                    self.job_manager.start(
                        job
                    )


                    job.status = JobStatus.RUNNING

                    job.update_progress(
                        5,
                        "Experiment started."
                    )


                    result = experiment_manager.run(
                        job.configuration,
                        job
                    )


                    job.update_progress(
                        100,
                        "Experiment completed."
                    )


                    job.finished_at = datetime.now()


                    self.job_manager.complete(
                        job,
                        result
                    )


            except Exception as error:


                self.job_manager.fail(
                    job,
                    str(error)
                )



        thread = Thread(
            target=worker,
            daemon=True
        )

        thread.start()


        return job.id



job_executor = JobExecutor()
